# ID Card Detection using YOLO, CNN, Python and OpenCV

A real-time computer vision system for monitoring student ID-card compliance.

## Overview
This project uses YOLO for real-time object detection and OpenCV for camera/video processing. An optional CNN classifier can be used as a second-stage verifier for detected ID-card regions.

The workflow captures frames, detects persons and ID cards, confirms repeated missing-card violations, sends up to three warning emails, and records a fine after the warning limit.

> Custom model weights and private student data are intentionally not included in this public repository.

## Technologies
- Python
- YOLO via Ultralytics
- CNN verification (optional)
- OpenCV
- NumPy
- SMTP email
- CSV logging

## Structure
```text
ID-Card-Detection-YOLO-CNN/
├── README.md
├── requirements.txt
├── .gitignore
├── config.example.py
├── src/
│   ├── main.py
│   ├── detector.py
│   ├── email_alert.py
│   └── violation_manager.py
├── models/README.md
├── dataset/README.md
├── screenshots/README.md
└── logs/.gitkeep
```

## Setup
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate it on Windows: `venv\\Scripts\\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `config.example.py` to `config.py` and update settings.
6. Place your trained custom YOLO model at `models/id_card_yolo.pt`.
7. Run: `python src/main.py`
8. Press Q to stop the camera.

## Email
For Gmail, use an App Password instead of your normal account password. Never commit real credentials. `config.py` is ignored by Git.

## Warning and Fine Logic
- Warning 1: email
- Warning 2: email
- Warning 3: email
- Next confirmed violation: fine recorded in `logs/fines.csv`

## Important
This is an academic prototype. The current demo uses a configurable student identifier and does not claim to identify individuals from faces. Institutional disciplinary actions should follow actual institutional policies and approvals.

## Future Enhancements
- Authorized ID-card OCR
- Database-backed student records
- Violation analytics dashboard
- Multi-person tracking
- CCTV stream support
- Privacy-aware identity matching
