from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
from PIL import Image
import io

app = FastAPI(title="BG Remover", description="Simple background removal tool")

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "BG Remover API", "status": "running"}

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    """Remove background from uploaded image"""
    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read uploaded image
        input_bytes = await file.read()
        
        # Remove background using rembg
        output_bytes = remove(input_bytes)
        
        # Return the processed image
        return Response(
            content=output_bytes,
            media_type="image/png",
            headers={
                "Content-Disposition": f'attachment; filename="{file.filename.rsplit(".", 1)[0]}_nobg.png"'
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Serve static files (frontend)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
