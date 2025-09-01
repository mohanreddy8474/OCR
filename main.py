from fastapi import WebSocket, FastAPI, File, UploadFile, Request, HTTPException
from starlette.websockets import WebSocketDisconnect
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from PIL import Image, ImageEnhance, ImageFilter
import io
import uvicorn
import asyncio
import os
import subprocess
import tempfile

app = FastAPI()
templates = Jinja2Templates(directory="frontend")

# Create uploads directory
os.makedirs("uploads", exist_ok=True)

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
                await asyncio.sleep(0.1)  # Small delay between messages
            except Exception:
                # Remove broken connections
                self.active_connections.remove(connection)

def check_tesseract_available():
    """Check if tesseract is available in the system"""
    try:
        subprocess.run(['tesseract', '--version'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def preprocess_image(image: Image.Image, enhance_contrast: bool = True, remove_noise: bool = True) -> Image.Image:
    """Simple image preprocessing for better OCR results"""
    try:
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        if enhance_contrast:
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.3)
            
            # Enhance brightness slightly
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.1)
        
        if remove_noise:
            # Simple noise reduction
            image = image.filter(ImageFilter.MedianFilter(3))
        
        # Convert to grayscale for better OCR
        image = image.convert('L')
        
        return image
    except Exception:
        return image

def extract_text_with_tesseract(image_path: str, language: str = "eng") -> str:
    """Extract text using tesseract command line"""
    try:
        # Create temporary file for output
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
            output_path = tmp_file.name
        
        # Run tesseract command
        cmd = ['tesseract', image_path, output_path.replace('.txt', ''), '-l', language]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Read the output
        with open(output_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Clean up temporary file
        os.unlink(output_path)
        
        return text.strip()
    except subprocess.CalledProcessError as e:
        raise Exception(f"Tesseract error: {e.stderr}")
    except Exception as e:
        raise Exception(f"Text extraction error: {str(e)}")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    language: str = "eng",
    enhance_contrast: bool = True,
    remove_noise: bool = True
):
    try:
        # Check if tesseract is available
        if not check_tesseract_available():
            raise HTTPException(status_code=500, detail="Tesseract OCR is not installed or not in PATH")
        
        # Validate file type
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')):
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        await manager.broadcast("Starting image upload...")
        
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        await manager.broadcast("Preprocessing image for better OCR...")
        
        # Preprocess image
        processed_image = preprocess_image(image, enhance_contrast, remove_noise)
        
        # Save processed image to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            temp_image_path = tmp_file.name
            processed_image.save(temp_image_path)
        
        try:
            await manager.broadcast("Beginning OCR processing...")
            
            # Extract text with language support
            extracted_text = extract_text_with_tesseract(temp_image_path, language)
            
            await manager.broadcast("Text extraction finished!")
            
            # Basic text cleaning
            cleaned_text = extracted_text.strip()
            
            # Calculate basic stats
            character_count = len(cleaned_text)
            word_count = len(cleaned_text.split()) if cleaned_text else 0
            line_count = len(cleaned_text.split('\n')) if cleaned_text else 0
            
            response = {
                "text": cleaned_text,
                "stats": {
                    "characters": character_count,
                    "words": word_count,
                    "lines": line_count
                },
                "language": language,
                "preprocessing": {
                    "enhance_contrast": enhance_contrast,
                    "remove_noise": remove_noise
                }
            }
            
            return response
            
        finally:
            # Clean up temporary image file
            if os.path.exists(temp_image_path):
                os.unlink(temp_image_path)
        
    except Exception as e:
        await manager.broadcast(f"Oops! An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Close WebSocket connections
        for connection in manager.active_connections:
            try:
                await connection.close()
            except Exception:
                pass

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/languages")
async def get_languages():
    """Get available languages"""
    try:
        if not check_tesseract_available():
            return {"languages": ["eng"]}
        
        # Get available languages from tesseract
        result = subprocess.run(['tesseract', '--list-langs'], capture_output=True, text=True)
        if result.returncode == 0:
            # Parse the output to get language codes
            lines = result.stdout.strip().split('\n')[1:]  # Skip first line
            languages = [line.strip() for line in lines if line.strip()]
            return {"languages": languages if languages else ["eng"]}
        else:
            return {"languages": ["eng"]}
    except Exception:
        return {"languages": ["eng"]}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    tesseract_available = check_tesseract_available()
    return {
        "status": "healthy" if tesseract_available else "unhealthy",
        "tesseract": "working" if tesseract_available else "not working"
    }

manager = ConnectionManager()

if __name__ == "__main__":
    print("🚀 Starting Improved OCR Application...")
    print("🌐 Server: http://localhost:8000")
    print("📱 Frontend: http://localhost:8000")
    print("🔍 API Docs: http://localhost:8000/docs")
    print("🏥 Health Check: http://localhost:8000/api/health")
    print("🌍 Languages: http://localhost:8000/api/languages")
    
    if not check_tesseract_available():
        print("⚠️  Warning: Tesseract OCR is not installed or not in PATH")
        print("   Please install Tesseract to use OCR functionality")
    else:
        print("✅ Tesseract OCR is available")
    
    print("Press Ctrl+C to stop")
    uvicorn.run(app, host="0.0.0.0", port=8000)
