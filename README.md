🧠 Object Detection, Tracking & Analytics Dashboard

A real-time object detection and tracking system using YOLOv8 + OpenCV, with automated CSV/JSON analytics and a React-based dashboard for visualizing counts and heatmaps.

This project captures live webcam video, detects and tracks objects (people & vehicles), generates analytics such as:

Total people & vehicles detected
Line-crossing count
FPS (Frames Per Second)
Movement heatmap
All analytics are saved automatically and visualized through a browser-based dashboard.

🏗️ Architecture
Webcam
  ↓
YOLOv8 Object Detection
  ↓
Object Tracking (ID-based)
  ↓
Analytics Generation
  ├─ CSV (summary)
  └─ JSON (heatmap + detailed data)
  ↓
FastAPI Backend
  ↓
React Dashboard (Charts + Heatmap)


🧰 Technologies Used
🔹 Backend (Python)
Python 3.11
YOLOv8 (Ultralytics) – Object Detection
OpenCV – Webcam capture & image processing
FastAPI – API server
Uvicorn – ASGI server
Pandas – CSV analytics
Matplotlib – Graph plotting (local)
NumPy

🔹 Frontend (React)
React (create-react-app)
HTML5 Canvas – Heatmap visualization
Fetch API – Backend communication

📂 Project Structure

object-detection-tracking/
│
├── app/
│   ├── api/            # FastAPI routes
│   ├── services/       # Detection, tracking, processing
│   ├── utils/          # Analytics & visualization
│   └── main.py         # FastAPI entry point
│
├── scripts/
│   └── run_webcam.py   # Webcam runner
│
├── data/
│   └── processed/
│       ├── analytics.csv
│       └── analytics.json
│
├── models/
│   └── yolov8n.pt
│
├── object-tracking-dashboard/
│   └── src/App.js      # React dashboard
│
├── requirements.txt
└── README.md
