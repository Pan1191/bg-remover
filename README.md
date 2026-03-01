# 🖼️ BG Remover - 去背小工具

Simple background removal tool powered by [rembg](https://github.com/danielgatis/rembg).

## Features

- 🎯 One-click background removal
- 📱 Mobile-friendly UI
- 🚀 Fast processing
- 🔒 No data stored - all processing in memory

## Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app:app --host 0.0.0.0 --port 8000
```

Then open http://localhost:8000 in your browser.

## API

### POST /remove-bg

Upload an image to remove its background.

**Request:** `multipart/form-data` with `file` field

**Response:** PNG image with transparent background

```bash
curl -X POST "http://localhost:8000/remove-bg" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@image.jpg" \
  --output removed_bg.png
```

## Tech Stack

- **Backend:** FastAPI + rembg (U²-Net)
- **Frontend:** Vanilla HTML/CSS/JS

## License

MIT
