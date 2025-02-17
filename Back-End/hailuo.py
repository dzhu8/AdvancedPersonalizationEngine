# This scrip has the functions to use the Hailuo API

import time
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Key and Endpoint
API_KEY = os.getenv("API_KEY")
GROUP_ID = os.getenv("GROUP_ID")  # Required for file retrieval

BASE_URL = "https://api.minimaxi.chat/v1"

# Video Parameters
MODEL = "T2V-01"  # Change to "I2V-01" for image-to-video
PROMPT = "A futuristic cityscape with flying cars and neon lights. [Pan left, Zoom in]"
OUTPUT_FILE = "generated_video.mp4"  # Name of the saved file

def create_video_generation_task(prompt, model="T2V-01"):
    """
    Sends a request to create a video generation task.
    """
    url = f"{BASE_URL}/video_generation"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "model": model
    }
    
    response = requests.post(url, headers=headers, json=payload)
    print(response.json())
    if response.status_code == 200:
        task_id = response.json().get("task_id")
        print(f"Video generation task submitted successfully. Task ID: {task_id}")
        return task_id
    else:
        print(f"Error: {response.json()}")
        return None

def query_video_status(task_id):
    """
    Checks the status of the video generation task.
    """
    url = f"{BASE_URL}/query/video_generation?task_id={task_id}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    print(response.json())
    if response.status_code == 200:
        data = response.json()
        status = data.get("status")
        file_id = data.get("file_id")
        print(f"Task Status: {status}")
        return status, file_id
    else:
        print(f"Error checking status: {response.json()}")
        return None, None

def download_video(file_id, output_filename="generated_video.mp4"):
    """
    Downloads the generated video using file_id.
    """
    url = f"{BASE_URL}/files/retrieve?GroupId={GROUP_ID}&file_id={file_id}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        download_url = response.json()["file"]["download_url"]
        print(f"Downloading video from: {download_url}")

        video_response = requests.get(download_url)
        with open(output_filename, "wb") as file:
            file.write(video_response.content)
        print(f"Video saved as {os.path.abspath(output_filename)}")
    else:
        print(f"Error downloading video: {response.json()}")

def test_api_connection():
    """
    Tests the API connection by making a simple request to check authentication.
    Returns True if connection is successful, False otherwise.
    """
    url = f"{BASE_URL}/query/credits"  # Using credits endpoint for testing
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("API Connection successful!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"API Connection failed. Status code: {response.status_code}")
            print(f"Error: {response.json()}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {str(e)}")
        return False

if __name__ == "__main__":
        
    # # Test API connection first
    # if not test_api_connection():
    #     print("Exiting due to API connection failure")
    #     exit(1)
        
    # # Step 1: Submit the video generation task
    # task_id = create_video_generation_task(PROMPT, MODEL)
    
    # if task_id:
    #     # Step 2: Poll for task completion
    #     while True:
    #         time.sleep(10)  # Wait 10 seconds before polling again
    #         status, file_id = query_video_status(task_id)

    #         if status == "Success" and file_id:
    #             # Step 3: Download the video
    #             download_video(file_id, OUTPUT_FILE)
    #             break
    #         elif status == "Fail":
    #             print("Video generation failed.")
    #             break
    print(query_video_status("238388714660066"))
