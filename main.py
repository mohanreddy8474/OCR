from fastapi import WebSocket, FastAPI, File, UploadFile, Request, HTTPException
from starlette.websockets import WebSocketDisconnect
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
import pytesseract
from PIL import Image
import io
import uvicorn
import asyncio

app = FastAPI()
templates = Jinja2Templates(directory="frontend")

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
            await asyncio.sleep(1)  # Sleep for 1 second between messages

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        await manager.broadcast("Starting image upload...")
        
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        await manager.broadcast("Beginning OCR processing...")
        
        extracted_text = pytesseract.image_to_string(image)
        
        await manager.broadcast("Text extraction finished!")
        
        response = {"text": extracted_text}
        
        for connection in manager.active_connections:
            await connection.close()
        
        return response
    except Exception as e:
        await manager.broadcast(f"Oops! An error occurred: {str(e)}")
        for connection in manager.active_connections:
            await connection.close()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
