from hailuo import (
    create_video_generation_task, 
    query_video_status, 
    download_video, 
    test_api_connection
)
import time

prompt = "Cute cat jumping"
output_file = "./videos/video_02.mp4"


def generate_and_download_video(prompt, output_file): 
    
    print("Starting video generation test...")
    print(f"Using prompt: {prompt}")
    
    # Create the video generation task
    task_id = create_video_generation_task(prompt)
   
    print(task_id)
    if not task_id:
        print("Failed to create video generation task")
        return
    
    print(f"Task created successfully. Task ID: {task_id}")
    print("Waiting for video generation to complete...")
    
    # Poll for completion
    while True:
        time.sleep(10)  # Wait 10 seconds between checks
        status, file_id = query_video_status(task_id)
        
        print(f"Current status: {status}")
        
        if status == "Success" and file_id:
            print("Video generation completed!")
            # Download the video
            download_video(file_id, output_file)
            break
        elif status == "Fail":
            print("Video generation failed.")
            break
        else:
            print("Still processing...")

if __name__ == "__main__":
    generate_and_download_video(prompt, output_file) 