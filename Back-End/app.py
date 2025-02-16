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