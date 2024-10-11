# OCR Web Application

This is a web application that performs Optical Character Recognition (OCR) on uploaded images using FastAPI, WebSockets, and Tesseract OCR.

## Features

- Upload image files for OCR processing
- Real-time status updates via WebSocket
- Display extracted text from images

## Prerequisites

- Python 3.7+
- FastAPI
- Starlette
- Jinja2
- pytesseract
- Pillow (PIL)
- uvicorn

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ocr-web-app.git
   cd ocr-web-app
   ```

2. Install the required packages:
   ```
   pip install fastapi starlette jinja2 pytesseract pillow uvicorn
   ```

3. Install Tesseract OCR on your system. Instructions may vary depending on your operating system.

## Usage

1. Run the FastAPI server:
   ```
   python zzz.py
   ```

2. Open a web browser and navigate to `http://localhost:8000`

3. Upload an image file and wait for the OCR processing to complete

4. View the extracted text in the result area

## File Structure

- `zzz.py`: Main FastAPI application file
- `templates/index.html`: HTML template for the web interface

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
-->
