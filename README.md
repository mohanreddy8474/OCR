# OCR Web Application

## Overview
This project is a web-based Optical Character Recognition (OCR) application that allows users to upload images and extract text from them. It uses FastAPI for the backend, WebSocket for real-time communication, and Tesseract OCR for text extraction.

## Features
- Image upload functionality
- Real-time progress updates via WebSocket
- Text extraction from uploaded images
- Simple web interface

## Tech Stack
- Backend: FastAPI, Python
- Frontend: HTML, JavaScript
- OCR: Tesseract
- WebSocket: FastAPI's WebSocket support

## Setup and Installation
1. Clone the repository
2. Install the required dependencies:
   ```
   pip install fastapi uvicorn python-multipart pillow pytesseract
   ```
3. Ensure Tesseract OCR is installed on your system
4. Run the application:
   ```
   python main.py
   ```

## Usage
1. Open a web browser and navigate to `http://localhost:8000`
2. Upload an image using the provided interface
3. Wait for the OCR process to complete
4. View the extracted text in the browser

## Project Structure
- `main.py`: Entry point of the application, contains all the FastAPI routes and WebSocket logic
- `frontend/`: Contains the HTML template for the web interface
