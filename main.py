from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
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

# API routes FIRST
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

# Serve index.html at root
@app.get("/")
async def root():
    return FileResponse("static/index.html")

# Serve other static files
app.mount("/static", StaticFiles(directory="static"), name="static")
