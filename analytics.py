import csv
import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# ===============================
# PATH SETUP (SAFE & ABSOLUTE)
# ===============================
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "processed"
CSV_FILE = DATA_DIR / "analytics.csv"
JSON_FILE = DATA_DIR / "analytics.json"

# Create directory ONCE
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ===============================
# SAVE ANALYTICS (CALLED PER FRAME)
# ===============================
def save_analytics(
    people,
    vehicles,
    line_count,
    fps,
    heat_points=None,
    zones=None
):
    record = {
        "timestamp": datetime.now().isoformat(),
        "people": people,
        "vehicles": vehicles,
        "line_crossed": line_count,
        "fps": round(float(fps), 2)
    }

    # 🔥 ADD HEATMAP POINTS (JSON ONLY)
    if heat_points is not None:
        record["heatmap"] = heat_points

    # 🔥 ADD ZONES (JSON ONLY)
    if zones is not None:
        record["zones"] = zones

    # ---------- JSON ----------
    if JSON_FILE.exists():
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(record)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    # ---------- CSV (UNCHANGED STRUCTURE) ----------
    file_exists = CSV_FILE.exists()
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["timestamp", "people", "vehicles", "line_crossed", "fps"]
        )
        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "timestamp": record["timestamp"],
            "people": people,
            "vehicles": vehicles,
            "line_crossed": line_count,
            "fps": record["fps"]
        })

# ===============================
# AUTO SUMMARY + GRAPHS (ON STOP)
# ===============================
def show_summary_and_plots():
    if not CSV_FILE.exists():
        print("❌ No analytics CSV found")
        return

    df = pd.read_csv(CSV_FILE)

    print("\n==============================")
    print("📊 SESSION ANALYTICS SUMMARY")
    print("==============================")
    print("Total frames captured :", len(df))
    print("Average FPS           :", round(df['fps'].mean(), 2))
    print("Max people detected   :", df['people'].max())
    print("Max vehicles detected :", df['vehicles'].max())
    print("Total line crossings  :", df['line_crossed'].sum())
    print("==============================\n")

    # ---- PEOPLE GRAPH ----
    plt.figure()
    plt.plot(df.index, df["people"])
    plt.title("People Count Over Time")
    plt.xlabel("Frame")
    plt.ylabel("People")
    plt.grid(True)
    plt.show()

    # ---- VEHICLE GRAPH ----
    plt.figure()
    plt.plot(df.index, df["vehicles"])
    plt.title("Vehicle Count Over Time")
    plt.xlabel("Frame")
    plt.ylabel("Vehicles")
    plt.grid(True)
    plt.show()

    # ---- FPS GRAPH ----
    plt.figure()
    plt.plot(df.index, df["fps"])
    plt.title("FPS Over Time")
    plt.xlabel("Frame")
    plt.ylabel("FPS")
    plt.grid(True)
    plt.show()
