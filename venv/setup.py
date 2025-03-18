import sqlite3

# Connect to SQLite database (or create if it doesn't exist)
conn = sqlite3.connect("wrinkle_detection.db")
cursor = conn.cursor()

# Create table for storing images and predictions
cursor.execute('''
    CREATE TABLE IF NOT EXISTS detections_temp (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_path TEXT NOT NULL,
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
''')

# Commit and close
conn.commit()
conn.close()
print("Database and table created successfully!")
