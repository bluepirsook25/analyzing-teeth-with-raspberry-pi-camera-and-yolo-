# Analyzing Teeth with Raspberry Pi Camera and YOLO

A computer vision project that uses YOLOv8 object detection with a Raspberry Pi camera to analyze and identify dental features in real-time.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Hardware Requirements](#hardware-requirements)
- [Configuration](#configuration)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project combines Raspberry Pi computing power with advanced computer vision using YOLOv8 to detect and analyze dental features from camera feeds. It's designed to process real-time video input and provide accurate object detection for dental analysis applications.

## ✨ Features

- **Real-time Detection**: Process video streams in real-time using YOLOv8
- **Raspberry Pi Optimized**: Lightweight implementation suitable for Raspberry Pi hardware
- **Custom Model Support**: Easy integration of custom-trained YOLO models
- **Image/Video Processing**: Support for both image files and video streams
- **Dental Feature Detection**: Trained to identify specific dental features and anomalies
- **Configurable Parameters**: Adjustable confidence thresholds and detection parameters

## 📦 Prerequisites

- Raspberry Pi 4B or higher (2GB RAM minimum, 4GB+ recommended)
- Python 3.8+
- Raspberry Pi Camera Module 2 or equivalent USB camera
- pip (Python package manager)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/bluepirsook25/analyzing-teeth-with-raspberry-pi-camera-and-yolo-.git
cd analyzing-teeth-with-raspberry-pi-camera-and-yolo-
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages include:
- `ultralytics` - YOLOv8 implementation
- `opencv-python` - Computer vision library
- `numpy` - Numerical computing
- `picamera2` or `picamera` - Raspberry Pi camera interface

### 4. Download Pre-trained Model

```bash
# Download YOLOv8 model (nano version recommended for Pi)
python3 -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

## 💻 Usage

### Basic Image Detection

```python
from ultralytics import YOLO

# Load model
model = YOLO('yolov8n.pt')

# Run inference
results = model.predict(source='path/to/image.jpg', conf=0.5)

# Process results
for result in results:
    print(result.boxes)
```

### Real-time Camera Feed

```python
# Check the dental_pc folder for real-time camera implementation
python3 dental_pc/main.py
```

### Video Processing

```python
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
results = model.predict(source='path/to/video.mp4', conf=0.5)
```

## 📂 Project Structure

```
analyzing-teeth-with-raspberry-pi-camera-and-yolo-/
├── dental_pc/                    # Main application folder
│   ├── main.py                   # Entry point
│   ├── camera_handler.py         # Camera interface
│   └── detection.py              # Detection logic
├── models/                       # Trained YOLO models
├── data/                         # Sample images/videos
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🔧 Hardware Requirements

- **Processor**: Raspberry Pi 4B (2GB minimum, 4GB recommended)
- **Camera**: Official Raspberry Pi Camera Module 2 or compatible USB camera
- **Storage**: Minimum 8GB microSD card (16GB+ recommended)
- **RAM**: 2GB minimum for inference (4GB for smoother operation)
- **Power Supply**: 5V/3A USB-C power adapter

## ⚙️ Configuration

Edit configuration parameters in your script:

```python
CONFIDENCE_THRESHOLD = 0.5        # Detection confidence
IOU_THRESHOLD = 0.45              # Non-max suppression IOU
MODEL_NAME = 'yolov8n.pt'         # Model variant (n/s/m/l/x)
CAMERA_INDEX = 0                  # Camera device index
```

## 📊 Results

Sample detection results will be saved in the `results/` folder with:
- Annotated images with bounding boxes
- Detection confidence scores
- Processing time metrics

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 📧 Contact & Support

For questions or support, please open an issue on the [GitHub repository](https://github.com/bluepirsook25/analyzing-teeth-with-raspberry-pi-camera-and-yolo-/issues).

---

**Created by**: bluepirsook25  
**Last Updated**: 2026-03-24