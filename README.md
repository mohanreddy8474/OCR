# 🔍 Improved OCR Application

A simple yet powerful OCR (Optical Character Recognition) application built with FastAPI and modern web technologies. Extract text from images with advanced preprocessing and multiple language support.

## ✨ Features

- **📁 Drag & Drop Upload**: Easy file upload with drag and drop support
- **🌍 Multi-Language Support**: Support for English, French, German, Spanish, Italian, Portuguese, and Russian
- **🖼️ Image Preprocessing**: Automatic contrast enhancement and noise reduction for better OCR results
- **📊 Real-time Status**: WebSocket-based real-time processing updates
- **📈 Text Statistics**: Character, word, and line count analysis
- **📋 Copy to Clipboard**: One-click text copying functionality
- **📱 Responsive Design**: Works perfectly on desktop and mobile devices
- **🎨 Modern UI**: Beautiful gradient design with smooth animations

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Tesseract OCR engine

### Installation

1. **Install Tesseract OCR**:
   ```bash
   # macOS
   brew install tesseract
   
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr
   
   # Windows
   # Download from: https://github.com/UB-Mannheim/tesseract/wiki
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

4. **Open your browser** and go to: `http://localhost:8000`

## 🛠️ How It Works

1. **Upload Image**: Drag and drop or click to select an image file
2. **Configure Options**: Choose language and preprocessing options
3. **Process**: Click "Process Image" to start OCR
4. **View Results**: See extracted text with statistics and copy to clipboard

## 🔧 API Endpoints

- `GET /` - Main application interface
- `POST /upload` - Process image with OCR
- `GET /api/languages` - Get available languages
- `GET /api/health` - Health check
- `WebSocket /ws` - Real-time status updates

## 📁 Project Structure

```
OCR/
├── main.py              # FastAPI backend application
├── frontend/
│   └── index.html      # Modern web interface
├── requirements.txt     # Python dependencies
├── uploads/            # Upload directory (auto-created)
└── README.md           # This file
```

## 🎯 Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)
- GIF (.gif)

## 🌍 Supported Languages

- English (eng)
- French (fra)
- German (deu)
- Spanish (spa)
- Italian (ita)
- Portuguese (por)
- Russian (rus)

## 🚀 Advanced Features

### Image Preprocessing
- **Contrast Enhancement**: Automatically improves text readability
- **Noise Reduction**: Removes image noise for cleaner OCR results
- **Grayscale Conversion**: Optimizes images for text recognition

### Real-time Updates
- WebSocket connection for live processing status
- Progress indicators and status messages
- Automatic connection management

### Text Analysis
- Character count
- Word count
- Line count
- Language detection

## 🔍 Troubleshooting

### Common Issues

1. **Tesseract not found**:
   - Ensure Tesseract is installed and in your PATH
   - Check installation with: `tesseract --version`

2. **Image processing errors**:
   - Verify image format is supported
   - Check image file isn't corrupted
   - Ensure image has readable text

3. **WebSocket connection issues**:
   - Check if port 8000 is available
   - Verify firewall settings

### Performance Tips

- Use high-quality images for better results
- Enable preprocessing options for noisy images
- Choose appropriate language for your text

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- OCR powered by [Tesseract](https://github.com/tesseract-ocr/tesseract)
- Image processing with [Pillow](https://python-pillow.org/)
- Modern UI with CSS Grid and Flexbox

---

**Happy Text Extraction! 🎉**
