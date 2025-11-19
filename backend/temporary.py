import sqlite3
from pathlib import Path

DB_PATH = Path("venv/wrinkle_detection.db")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Add the column without default (SQLite doesn't allow CURRENT_TIMESTAMP in ALTER TABLE)
cursor.execute("ALTER TABLE detections ADD COLUMN image_path_timestamp TEXT")

# Update existing rows with current timestamp
cursor.execute("UPDATE detections SET image_path_timestamp = datetime('now') WHERE image_path_timestamp IS NULL")

conn.commit()
conn.close()
print("Column added successfully!")