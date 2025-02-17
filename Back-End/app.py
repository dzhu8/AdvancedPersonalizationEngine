from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from openai_helper import OpenAIHelper

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI helper
openai_helper = OpenAIHelper()

@app.post("/process-screenshot")
async def process_screenshot(   
    file: Optional[UploadFile] = None,
    file_url: Optional[str] = Form(None), 
    brand_instructions: Optional[str] = Form(None)
):
    if file is None and not file_url:
        return {"error": "No file or file URL provided"}
    
    try:
        # If file is uploaded, use the file data
        if file:
            file_data = await file.read()
            analysis = await openai_helper.analyze_file(
                file_data,
                filename=file.filename,
                instructions=brand_instructions
            )
        # If URL is provided, pass it directly to OpenAI
        else:
            analysis = await openai_helper.analyze_file(
                file_url,
                instructions=brand_instructions
            )
        
        return {
            "analysis": analysis,
            "brand_instructions": brand_instructions
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/process-prompt")
async def process_prompt(
    previous_analysis: str = Form(...),
    followup_prompt: str = Form(...)
):
    try:
        analysis = await openai_helper.process_followup(
            previous_analysis,
            followup_prompt
        )
        
        return {
            "analysis": analysis
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/generate-storyboard")
async def generate_storyboard(
    file: UploadFile,
    instructions: Optional[str] = Form(None)
):
    """
    Generate a complete storyboard from an uploaded image
    """
    try:
        file_data = await file.read()
        result = await openai_helper.generate_complete_storyboard(
            file_data,
            filename=file.filename,
            instructions=instructions
        )
        
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def root():
    return {"message": "Welcome to the File Processing API"}


@app.get("/serve-video")
async def serve_video(filepath: str = None, directory: str = None):
    """
    Serves a video file to be displayed on the frontend.

    Args:
        filepath: The full path to a video file to be served.
        directory: A directory path in which to search for video files generated within
            the past 10 seconds. If multiple are found, the most recent one is used.

    Returns:
        A FileResponse sending back the video file.
    """
    if filepath:
        # If a specific file path is provided, check its existence.
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(filepath, media_type="video/mp4", filename=os.path.basename(filepath))

    elif directory:
        if not os.path.isdir(directory):
            raise HTTPException(status_code=400, detail="Provided directory is not valid")

        now = time.time()
        recent_files = []
        for file in os.listdir(directory):
            full_path = os.path.join(directory, file)
            if os.path.isfile(full_path):
                mod_time = os.path.getmtime(full_path)
                # Check if file was modified within the last 10 seconds
                if now - mod_time <= 10:
                    recent_files.append((full_path, mod_time))

        if not recent_files:
            raise HTTPException(status_code=404, detail="No video file generated in the past 10 seconds found in directory")

        # Sort files by modification time in descending order
        recent_files.sort(key=lambda x: x[1], reverse=True)
        latest_file = recent_files[0][0]
        return FileResponse(latest_file, media_type="video/mp4", filename=os.path.basename(latest_file))

    else:
        raise HTTPException(status_code=400, detail="Either 'filepath' or 'directory' must be provided")
