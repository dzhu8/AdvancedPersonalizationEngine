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
            # Create JSON directory if it doesn't exist
            json_dir = os.path.join(os.path.dirname(__file__), 'json')
            os.makedirs(json_dir, exist_ok=True)

            # Check if storyboard already exists for this file
            base_name = filename.rsplit('.', 1)[0]
            json_filename = os.path.join(json_dir, f"{base_name}_storyboard.json")
            
            try:
                with open(json_filename, 'r') as f:
                    existing_storyboard = f.read()
                    scenes = StoryboardGenerator.validate_storyboard_json(existing_storyboard)
                    # Generate the final video from the storyboard
                    final_video = self.generate_videos_from_storyboard(scenes)
                    return final_video
                
            except (FileNotFoundError, ValueError):
                # Proceed with new storyboard generation if file doesn't exist
                # or is invalid JSON
                pass
            
            # Step 1: Initial image analysis
            initial_analysis = await self.analyze_file(file_input, filename, instructions)
            
            # Step 2: Generate storyboard
            storyboard_prompt = StoryboardGenerator.get_default_storyboard_prompt()
            storyboard_json = await self.process_followup(initial_analysis, storyboard_prompt)
            print(storyboard_json)
        
            # Write to JSON file in the dedicated directory
            with open(json_filename, 'w') as f:
                f.write(storyboard_json)
            # Step 3: Validate and parse the storyboard
            scenes = StoryboardGenerator.validate_storyboard_json(storyboard_json)
            print(scenes)
            
            # Generate the final video from the storyboard
            final_video = self.generate_videos_from_storyboard(scenes)
            return final_video
            
        except Exception as e:
            raise Exception(f"Error generating storyboard: {str(e)}") 
        
    def generate_videos_from_storyboard(self, storyboard_json):
        """
        Generates videos for each scene in the storyboard and combines them.
        
        Args:
            storyboard_json (dict): JSON containing scene descriptions
            
        Returns:
            str: Path to the final combined video file, or None if generation fails
        """
        from hailuo import create_video_generation_task, query_video_status, download_video
        import time
        import os
        
        video_files = []
        # Generate video for each scene (testing with first 2 scenes only)
        for scene_num, scene_data in list(storyboard_json.items()):
            print(f"\nProcessing {scene_num}...")
            
            # Construct prompt from scene data
            prompt = f"""
            {scene_data}
            """
            
            # Generate video for this scene
            timestamp = int(time.time())
            output_file = os.path.join("./videos/tmp_videos", f"scene_{scene_num}_{timestamp}.mp4")
            

            print(prompt)
            # Step 1: Create video generation task
            task_id = create_video_generation_task(prompt)
            print(task_id)
            if task_id:
                # Step 2: Poll for completion
                while True:
                    time.sleep(1)  # Wait between status checks
                    status, file_id = query_video_status(task_id)
                    
                    if status == "Success" and file_id:
                        # Step 3: Download the video
                        download_video(file_id, output_file)
                        video_files.append(output_file)
                        break
                    elif status == "Fail":
                        print(f"Video generation failed for {scene_num}")
                        break
            else:
                print(f"Failed to create video generation task for {scene_num}")
        

        #video_files = ["./videos/tmp_videos/test_video_01.mp4", "./videos/tmp_videos/test_video_02.mp4"]
        if not video_files:
            print("No videos were successfully generated")
            return None
        
        # Combine videos if more than one was generated
        if len(video_files) > 1:
            try:
                from moviepy import VideoFileClip, concatenate_videoclips
                
                # Load all video clips
                clips = [VideoFileClip(file) for file in video_files]
                
                # Concatenate clips
                final_clip = concatenate_videoclips(clips)
                
                # Write final video
                output_path = f"./videos/merged_video.mp4"
                final_clip.write_videofile(output_path)
                
                # Close clips
                for clip in clips:
                    clip.close()
                
                return output_path
                
            except Exception as e:
                print(f"Error combining videos: {str(e)}")
                return video_files[0]  # Return first video if combination fails
        
        # If only one video was generated, return its path as a string
        # Returns str: Path to the generated video file (e.g. "./videos/tmp_videos/test_video_01.mp4")
        return video_files[0]

