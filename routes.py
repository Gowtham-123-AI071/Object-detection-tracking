from fastapi import APIRouter
from fastapi.responses import FileResponse, StreamingResponse
from pathlib import Path
import json

from app.services.video_processor import VideoProcessor

router = APIRouter()
processor = VideoProcessor()

# ===============================
# PATH SETUP
# ===============================
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "processed"
CSV_FILE = DATA_DIR / "analytics.csv"
JSON_FILE = DATA_DIR / "analytics.json"

# ===============================
# LIVE VIDEO STREAM (OPTIONAL)
# ===============================
@router.get("/video")
def video_feed():
    return StreamingResponse(
        processor.process_webcam_stream(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

# ===============================
# DOWNLOAD CSV ANALYTICS
# ===============================
@router.get("/analytics/csv")
def download_csv():
    return FileResponse(
        CSV_FILE,
        filename="analytics.csv",
        media_type="text/csv"
    )

# ===============================
# GET JSON ANALYTICS
# ===============================
@router.get("/analytics/json")
def analytics_json():
    if JSON_FILE.exists():
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []
