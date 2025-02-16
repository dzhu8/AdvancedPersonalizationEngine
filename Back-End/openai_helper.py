import base64
from openai import OpenAI
import os
from typing import Optional, Union, Dict, Any
from dotenv import load_dotenv
import mimetypes
from storyboard_generator import StoryboardGenerator

class OpenAIHelper:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Verify API key is present
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found in environment variables")
            
        self.client = OpenAI()

    def encode_image_to_base64(self, image_data: bytes) -> str:
        """Convert image bytes to base64 string"""
        return base64.b64encode(image_data).decode('utf-8')

    def get_mime_type(self, file_data: bytes, filename: str) -> str:
        """Determine the MIME type of the file"""
        mime_type, _ = mimetypes.guess_type(filename)
        return mime_type

    async def analyze_file(self, file_input: Union[str, bytes], filename: str = None, instructions: Optional[str] = None) -> str:
        """
        Analyze a file (image or PDF) using OpenAI's API
        
        Args:
            file_input: Either a URL string or file bytes
            filename: Name of the file (used to determine type)
            instructions: Optional instructions for analysis
        """
        default_prompt = """I want to create a hyper-personalized advertisement based on an individual's Instagram profile. I will provide a selection of their pictures. Analyze these images and extract detailed insights about their personality, lifestyle, aesthetic, and brand affinity. Your analysis should cover the following key aspects: 
Interests & Activities - Identify their hobbies, passions, and frequently engaged activities. 
Visual Aesthetic & Color Palette - Describe the dominant tones, styling, and mood of their content. 
Fashion & Personal Style - Note recurring clothing choices, accessories, and branding cues that define their fashion identity. 
Brand Affinity & Product Preferences - Identify any brands, sponsorships, or frequently featured products in their posts. Location & Setting Preferences – Analyze recurring backdrops to determine preferred environments. 
Personality & Expression - Examine facial expressions, body language, and engagement style. 
Social & Lifestyle Indicators - Determine whether they engage in solo activities, group settings, family-oriented content, or influencer collaborations. 
Emotional Tone & Vibe - Identify the overall emotional feel of their posts. 
Media Type & Engagement Style - Note whether their content is video-heavy, photo-centric, or focused on reels/stories and analyze engagement style. 
Potential Advertising Angles - Based on the extracted insights, suggest the best tone, visual style, and storytelling approach for a hyper-personalized ad that aligns naturally with their profile and resonates with their audience. 
The goal is to extract deep insights from their Instagram content to craft an AI-generated video that seamlessly integrates with their aesthetic, lifestyle, and personality, making the advertisement feel natural, authentic, and engaging.
"""

        prompt = instructions if instructions else default_prompt
        try:
            # Handle different file types
            if isinstance(file_input, str):
                # It's a URL
                if file_input.startswith(('http://', 'https://')):
                    return await self._analyze_image_url(file_input, prompt)
                else:
                    raise ValueError("Invalid URL provided")
            else:
                # It's file data
                mime_type = self.get_mime_type(file_input, filename)
                
                if mime_type and mime_type.startswith('image/'):
                    return await self._analyze_image_data(file_input, prompt)
                elif mime_type == 'application/pdf':
                    return await self._analyze_pdf(file_input, prompt)
                else:
                    raise ValueError(f"Unsupported file type: {mime_type}")

        except Exception as e:
            return f"Error analyzing file: {str(e)}"

    async def _analyze_image_url(self, url: str, prompt: str) -> str:
        """Handle image URL analysis"""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": url},
                        },
                    ],
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content

    async def _analyze_image_data(self, image_data: bytes, prompt: str) -> str:
        """Handle image data analysis"""
        base64_image = self.encode_image_to_base64(image_data)
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content

    async def _analyze_pdf(self, pdf_data: bytes, prompt: str) -> str:
        """Handle PDF analysis"""
        # Upload the PDF file
        file_response = self.client.files.create(
            file=pdf_data,
            purpose='assistants'
        )

        # Create an assistant with the uploaded PDF
        assistant = self.client.beta.assistants.create(
            name="Document Assistant",
            instructions=prompt,
            model="gpt-4",
            tools=[{"type": "retrieval"}],
            file_ids=[file_response.id]
        )

        # Create a thread
        thread = self.client.beta.threads.create()

        # Add a message to the thread
        message = self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content="Please analyze this document according to the instructions provided."
        )

        # Run the assistant
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        # Wait for completion and get the response
        while True:
            run_status = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == 'completed':
                messages = self.client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                return messages.data[0].content[0].text.value
            elif run_status.status in ['failed', 'cancelled']:
                return f"Analysis failed: {run_status.status}"

        return "Analysis completed"

    async def process_followup(self, previous_analysis: str, followup_prompt: str) -> dict:
        """Process a followup prompt based on previous analysis and return JSON"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an AI specialized in creating personalized advertising content."},
                    {"role": "user", "content": "Here is the analysis of someone's Instagram profile:\n\n" + previous_analysis},
                    {"role": "user", "content": followup_prompt}
                ],
                response_format={ "type": "json_object" },
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return {"error": f"Error processing followup: {str(e)}"}

    async def generate_complete_storyboard(
        self,
        file_input: Union[str, bytes],
        filename: str = None,
        instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Complete workflow to analyze an image and generate a storyboard
        
        Args:
            file_input: Either a URL string or file bytes
            filename: Name of the file (used to determine type)
            instructions: Optional custom instructions for initial analysis
            
        Returns:
            Dict containing both the initial analysis and storyboard scenes
        """
        try:
            # Step 1: Initial image analysis
            initial_analysis = await self.analyze_file(file_input, filename, instructions)
            
            # Step 2: Generate storyboard
            storyboard_prompt = StoryboardGenerator.get_default_storyboard_prompt()
            storyboard_json = await self.process_followup(initial_analysis, storyboard_prompt)
            
            # Step 3: Validate and parse the storyboard
            scenes = StoryboardGenerator.validate_storyboard_json(storyboard_json)
            
            return {
                "initial_analysis": initial_analysis,
                "scenes": scenes
            }
            
        except Exception as e:
            raise Exception(f"Error generating storyboard: {str(e)}") 