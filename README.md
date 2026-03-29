# 🛡️ Real-Time Threat Detection System

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=flat&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-hand--tracking-blue)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Object_Detection-orange)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=flat&logo=PyTorch&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

## 📌 Architectural Overview & Analysis

Welcome to the **Real-Time Threat Detection System**, an AI-powered surveillance anomaly detection system built strictly with modern computer vision standards. 

As a Senior Software Engineer analyzing this project, here is an anatomical breakdown of its robust and modular design:

1. **Modular Architecture**: The codebase is cleanly decoupled into `modules/`, `utils/`, and a primary execution layer (`main.py`). This allows individual components like `HandTracker` or `ObjectDetector` to be scaled, tested, or swapped seamlessly without breaking the monolithic structure.
2. **Multi-Model Concurrency**: The system intelligently runs two separate YOLOv8 models (`yolov8s` robust COCO pre-trained base model & a custom-trained model for edge-cases like the *hammer*) concurrently.
3. **Context-Aware Spatio-Temporal Logic**: Instead of relying purely on object detection which throws false positives if a knife is simply lying passively on a table, the `ThreatAnalyzer` uses Euclidean distance geometry mapping between MediaPipe Hand Landmarks (specifically Landmark 8 - Index Finger Tip) and the bounding box center of the dangerous objects. If the $distance < 80px$ threshold is crossed, it escalates to a threat.
4. **Asynchronous I/O Operations**: Audio alarms (`pyttsx3`) are decoupled using Python `threading`. This prevents the main rendering thread from experiencing I/O blocking, maintaining a smooth framerate (FPS) during a threat event.
5. **Comprehensive Audit Trails**: The `logger.py` ensures that all incidents leave an immutable trail. Actionable logs, full-frame snapshots (Evidences), and rolling 7-second video clips are systematically captured directly to the file system.

## ✨ Features

- **Real-Time Hand & Object Tracking**: Employs MediaPipe for robust sub-millisecond hand mapping and YOLOv8 for precise multi-object boundary encapsulation.
- **Contextual Threat Evaluation**: A knife resting on a counter isn't necessarily a threat. A knife held in a physical hand is. This real-world contextual validation dramatically reduces false positive rates.
- **Dynamic Security Dashboard**: Overlays a futuristic UI on the video feed tracking active object counts, hand counts, system health, and FPS in real-time.
- **Acoustic Warning System**: Automated text-to-speech sirens blare upon detection asynchronously.
- **Automated Evidence Collection**: 
   - 📸 Snapshot of the exact threat frame saved to `evidences/`
   - 🎥 7-second video recording buffer of the incident.
   - 📝 Detailed `.txt` logs appending timestamps and AI confidence scores into `logs/threat_logs.txt`.
   - **📱 Instant Telegram Alerts**: Asynchronously pushes the evidence snapshot and a warning message directly to your mobile device via the Telegram API without dropping webcam FPS.

## 🏗️ Project Structure

```text
ThreatDetectionProject/
│
├── main.py                   # Core execution loop & UI renderer
├── requirements.txt          # Extensive Python dependencies list
├── README.md                 # Project documentation
├── LICENSE                   # MIT License
├── .env                      # Template for Telegram API keys
├── evidences/                # Auto-generated images and video clips of threats
├── logs/                     # Auto-generated text audits of threat logs
├── models/                   
│   ├── yolov8s.pt            # Base YOLOv8 small model
│   └── hammer.pt             # Custom fine-tuned YOLO model 
├── modules/                  
│   ├── object_detector.py    # YOLOv8 implementation inference
│   ├── hand_tracker.py       # MediaPipe abstraction layer
│   └── threat_analyzer.py    # Euclidean distance logical processor
└── utils/                    
    ├── logger.py             # I/O logging & Video/Image persistence wrappers
    └── notifier.py           # Telegram bot async integration layer
```

## 🚀 Installation & Setup

### Requirements

Ensure you have Python 3.8+ installed. It is highly recommended to allocate a fresh virtual environment before pulling the dependencies.

```bash
# Clone the repository (if applicable)
git clone https://github.com/ddemi-ssena/Real-Time-Threat-Detection-System.git
cd Real-Time-Threat-Detection-System

# Create and activate a Virtual Environment
python -m venv venv
# On Windows use: 
venv\Scripts\activate
# On macOS/Linux use: 
# source venv/bin/activate

# Install the dependencies
pip install -r requirements.txt
```

### 📱 Setting Up Telegram Notifications (Optional but Recommended)

To receive real-time snapshots of threats directly to your phone:
1. Search specifically for **`@BotFather`** on Telegram and create a new bot using `/newbot`. Copy the API Token.
2. Search for **`@userinfobot`** on Telegram and click Start to get your numeric Chat ID.
3. Rename the `.env.example` file in the project root to `.env`.
4. Populate the fields with your credentials:
```env
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### Running the System

Execute the main controller process. Ensure your designated web-camera is active and correctly configured to `cv2.VideoCapture(0)`.

```bash
python main.py
```

*Press `q` within the application window frame to elegantly shutdown the system and cleanly release OpenCV VideoWriter I/O buffers.*

## 🧠 Core Processing Pipeline Walkthrough

1. **Frame Capture Layer**: Reads standard continuous BGR frames from the physical webcam feed via OpenCV mapping.
2. **Inference Pipeline Layer**:
   - `HandTracker` transforms the BGR matrix to RGB and computes 21 coordinate points of the human hand architecture.
   - `ObjectDetector` feeds the raw source down the YOLO backbone isolating high-risk targets (person, knife, scissors, hammer).
3. **Data Fusion & Analytical Matrix**: The `ThreatAnalyzer.calculate_threat()` loops `O(h * o)` where `h` is total hands logic and `o` is total objects logic, measuring relative spatial correlation across the X-Y pixel coordinate plane.
4. **Trigger & Event Feedback Loop**: When a positional overlapping event triggers a positive anomaly, it commands the hardware subsystem to dump (Logs + Snapshot Imaging + Video Writer Buffer Allocation + Voice Alarm).

## 📄 License & Usage

This robust system is open-source software built for educational and demonstrative security enhancement purposes. It is licensed under the [MIT License](LICENSE) - dive into the LICENSE file for more comprehensive details.
