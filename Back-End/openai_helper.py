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
        print("Calling analyze_file")

        default_prompt = """Your job is to study the images and derive general insights about their personality, lifestyle, aesthetic,
and brand preferences. While doing so, please respect their privacy and avoid disclosing any personal
identifiable information.

Specifically, from the provided images, focus on these key aspects:

1. Interests & Activities:
  - Identify recurring hobbies, passions, and activities that appear in their photos.

2. Visual Aesthetic & Color Palette:
  - Describe the dominant colors, styling, and ambiance that define their overall image aesthetic.

3. Fashion & Personal Style:
  - Note recurring clothing choices, accessories, or visible brand elements that reflect their style.

4. Brand Affinity & Product Preferences:
  - Observe any featured brands, sponsorships, or products that appear consistently across their photos.
 
5. Location & Setting Preferences:
  - Identify common backdrops or environments (e.g., urban, nature, home settings) that the individual
    seems to prefer.

6. Personality & Expression:
  - Examine facial expressions, body language, or other cues that might suggest personality traits
    or an overall vibe.

7. Social & Lifestyle Indicators:
  - Determine whether they appear with friends, family, or in group settings, or if they tend
    to take solo photos.

8. Emotional Tone & Mood:
  - Identify the emotional feel of their content—e.g., playful, adventurous, calm, or energetic.

9. Media Type & Engagement Style:
  - Note whether the user prefers short videos, still images, reels/stories, etc., and speculate
    on their engagement style.

10. Advertising Angles:
  - Based on these observations, propose the most suitable advertising angle, including
    visual style, storytelling approach, and tone that would fit naturally with their
    personality and aesthetic.

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
            max_tokens=1500,
        )
        print(response.choices[0].message.content)
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
            max_tokens=1500,
        )
        print(response.choices[0].message.content)
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
        print("Calling process_followup")
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an AI specialized in creating personalized advertising content."},
                    {"role": "user", "content": "Here is the analysis:\n\n" + previous_analysis},
                    {"role": "user", "content": followup_prompt}
                ],
                response_format={ "type": "json_object" },
                max_tokens=1500
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
        print("Calling generate_complete_storyboard")
        try:
            # Step 1: Initial image analysis
            import pdb; pdb.set_trace()
            initial_analysis = await self.analyze_file(file_input, filename, instructions)
            
            # Step 2: Generate storyboard
            import pdb; pdb.set_trace()
            storyboard_prompt = StoryboardGenerator.get_default_storyboard_prompt()
            storyboard_json = await self.process_followup(initial_analysis, storyboard_prompt)
            print(storyboard_json)
            
            # Step 3: Validate and parse the storyboard
            import pdb; pdb.set_trace()
            scenes = StoryboardGenerator.validate_storyboard_json(storyboard_json)
            print(scenes)
            
            return {
                "initial_analysis": initial_analysis,
                "scenes": scenes
            }
            
        except Exception as e:
            raise Exception(f"Error generating storyboard: {str(e)}") 