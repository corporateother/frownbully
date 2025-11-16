from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

DB_PATH = Path(__file__).resolve().parent.parent / "venv" / "wrinkle_detection.db"

@dataclass(frozen=True)
class DailyCount:
    date: datetime
    count: int

def _connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)

def ensure_database_exists() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"SQLite database not found at {DB_PATH}")

def count_rows_between(start: datetime, end: datetime) -> int:
    ensure_database_exists()
    query = """
        SELECT COUNT(*)
        FROM detections
        WHERE datetime(image_path_timestamp) >= ? AND datetime(image_path_timestamp) < ?
    """
    with _connect() as conn:
        cursor = conn.execute(query, (start.isoformat(), end.isoformat()))
        return cursor.fetchone()[0]

def daily_counts(days: int) -> List[DailyCount]:
    ensure_database_exists()
    cutoff = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    history: List[DailyCount] = []
    for offset in range(days, -1, -1):
        day_start = cutoff - timedelta(days=offset)
        day_end = day_start + timedelta(days=1)
        history.append(DailyCount(date=day_start, count=count_rows_between(day_start, day_end)))
    return history

def summary() -> Dict[str, Any]:
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today_start - timedelta(days=1)
    week_start = today_start - timedelta(days=today_start.weekday())
    last_week_start = week_start - timedelta(days=7)

    return {
        "today": count_rows_between(today_start, today_start + timedelta(days=1)),
        "yesterday": count_rows_between(yesterday_start, today_start),
        "thisWeek": count_rows_between(week_start, week_start + timedelta(days=7)),
        "lastWeek": count_rows_between(last_week_start, week_start),
        "history": [
            {"label": day.date.strftime("%b %d"), "count": day.count}
            for day in daily_counts(6)
        ],
    }