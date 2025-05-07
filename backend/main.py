from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import numpy as np
from typing import List
import os
from datetime import datetime
import shutil

app = FastAPI(title="TumorLens API", description="Brain Tumor Detection API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Welcome to TumorLens API"}

@app.post("/upload/")
async def upload_mri(file: UploadFile = File(...)):
    """
    Upload an MRI scan for analysis
    """
    try:
        # Create a unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # TODO: Add preprocessing and model inference here
        
        return {
            "message": "File uploaded successfully",
            "filename": filename,
            "status": "pending_analysis"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analysis/{filename}")
async def get_analysis(filename: str):
    """
    Get the analysis results for a previously uploaded MRI scan
    """
    # TODO: Implement analysis retrieval
    return {
        "filename": filename,
        "status": "analysis_not_implemented",
        "message": "Analysis endpoint is under development"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 