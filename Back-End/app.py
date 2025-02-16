from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process-screenshot")
async def process_screenshot(   
    image: UploadFile = None, 
    brand_instructions: Optional[str] = Form(None)
):
    if image is None:
        return {"error": "No image provided"}
    
    # For now, we just return hello world and the instructions if provided
    response = {"message": "Hello World"}
    if brand_instructions:
        response["brand_instructions"] = brand_instructions
    
    return response

@app.get("/")
async def root():
    return {"message": "Welcome to the Image Processing API"} 