import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "venv" / "wrinkle_detection.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)  # ensure folder exists

# Connect to SQLite database (or create if it doesn't exist)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

#Create table for storing predictions
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS detections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_path TEXT NOT NULL,
        image_path_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        bunny_line DECIMAL(5,4),
        chin DECIMAL(5,4),
        crows_feet DECIMAL(5,4),
        forehead DECIMAL(5,4),
        frown_line DECIMAL(5,4),
        gummy_smile DECIMAL(5,4),
        masseter DECIMAL(5,4),
        sad_smile DECIMAL(5,4),
        smoker_lines DECIMAL(5,4),
        notification TEXT CHECK(notification IN ('YES', 'NO')),
        notification_threshold DECIMAL(5,4)
    )
    """
)
# Commit and close
conn.commit()
conn.close()
print("Database and table created successfully!")