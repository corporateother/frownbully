import cv2
import time
import subprocess
import logging
import os
import base64
import re
import sys
import sqlite3
import threading
from datetime import datetime
from pathlib import Path
from plyer import notification
import frown_stats as stats

# --- GLOBAL STATE AND CONFIGURATION ---
# State variable to control the detection loop
DB_PATH = Path(__file__).resolve().parent.parent / "venv" / "wrinkle_detection.db"
BASE_DIR = Path(__file__).resolve().parent

# Generate a unique log file with timestamp
log_filename = f"script_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Ensure the log file is created in a relative path to where the script is run
logging.basicConfig(
    filename=os.path.join(BASE_DIR, log_filename),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

detection_running = False
detection_thread = None
stats_data = {"last_detection": "N/A", "status": "Stopped", "latest_prediction": {}, "summary": stats.summary()}

# --- CORE APPLICATION LOOP (RUNS IN SEPARATE THREAD) ---

def continuous_detection_loop():
    """The main loop that captures, processes, and notifies."""
    global detection_running
    logging.info("Continuous detection loop started.")

    while detection_running:
        try:
            time.sleep(1)  # Capture image every 1s

            # 1. Capture Image
            image_path = capture_image()
            if not image_path:
                continue

            # 2. Run Inference
            raw_results = run_inference(image_path)
            if raw_results is None:
                continue

            # 3. Parse and Save Predictions
            parsed_results = parse_results(raw_results)
            if parsed_results:
                save_predictions_to_db(image_path, parsed_results)
            else:
                logging.warning(f"No predictions found for {image_path}, skipping database update.")

            # 4. Notify User
            notify_user(parsed_results)

            # 5. Update Global Stats for API access
            global stats_data
            stats_data["last_detection"] = datetime.now().strftime("%H:%M:%S")
            stats_data["latest_prediction"] = parsed_results
            stats_data["status"] = "Running"

        except Exception as e:
            logging.error(f"Error inside detection loop: {e}")
            # Prevents thread from crashing on error
            time.sleep(2)

    logging.info("Continuous detection loop terminated.")
    # Reset status when loop exits
    stats_data["status"] = "Stopped"


# --- API EXPOSED FUNCTIONS ---

def start_detection():
    """Starts the continuous detection loop in a background thread."""
    global detection_running, detection_thread
    if not detection_running:
        detection_running = True
        detection_thread = threading.Thread(target=continuous_detection_loop)
        detection_thread.daemon = True  # Allows program to exit even if thread is running
        detection_thread.start()
        logging.info("Detection started and thread launched.")
        return True
    return False


def stop_detection():
    """Stops the continuous detection loop."""
    global detection_running, detection_thread
    if detection_running:
        detection_running = False
        # Optional: wait for the thread to finish cleanly if needed, but not essential here
        if detection_thread and detection_thread.is_alive():
            # Wait a short time for the thread to shut down
            detection_thread.join(timeout=1)
        detection_thread = None
        logging.info("Detection stopped.")
        return True
    return False


def is_running():
    """Returns the current running status."""
    global detection_running
    return detection_running


def get_stats():
    formatted_predictions = {
        label: f"{confidence * 100:.2f}%"
        for label, confidence in stats_data['latest_prediction'].items()
    }
    return {
        "running": is_running(),
        "last_detection": stats_data["last_detection"],
        "status": stats_data["status"],
        "latest_prediction": formatted_predictions,
        "summary": stats.summary(),
    }


# --- REST OF ORIGINAL LOGIC (Unchanged) ---
# Image Capturing
def capture_image(max_retries=3):
    # Define the folder path in AppData (No admin permission required)
    appdata_path = os.getenv('LOCALAPPDATA')
    if not appdata_path:
        logging.error("LOCALAPPDATA environment variable is not set.")
        return None

    folder_path = os.path.join(appdata_path, "frownbully", "detections")

    try:
        os.makedirs(folder_path, exist_ok=True)  # Ensure folder creation
        logging.info(f"Folder ensured at: {folder_path}")
    except Exception as e:
        logging.error(f"Failed to create folder {folder_path}: {e}")
        return None

    # Generate a timestamp-based filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = os.path.join(folder_path, f"{timestamp}.jpg")

    logging.info("Capturing image from webcam.")
    cap = cv2.VideoCapture(0)

    for attempt in range(max_retries):
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(image_path, frame)
            logging.info(f"Image captured successfully: {image_path}")
            cap.release()

            # Save image path to database
            save_image_to_db(image_path)

            # HACK: Fix the indentation error here
            return image_path
        else:
            logging.warning(f"Attempt {attempt + 1}: Failed to capture image. Retrying...")
            time.sleep(1)

    # Indentation fix: The 'captured_image_path' and 'if not os.path.exists' block was incorrect
    # Removed the redundant inner call to capture_image()

    logging.error("Failed to capture image after multiple attempts.")
    cap.release()
    return None


# Function to save image path in the database
def save_image_to_db(image_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
      """
      INSERT INTO detections (image_path, image_path_timestamp)
      VALUES (?, ?)
      """,
      (image_path, datetime.now().isoformat()),
    ) 
    conn.commit()
    conn.close()
    logging.info(f"Image path saved to database: {image_path}")


# Ensure the path is correctly formatted
def encode_image(image_path):
    image_path = os.path.normpath(image_path)  # Normalize path
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        logging.error(f"Error: Image file not found at {image_path}")
        # Removed redundant re-raise: raise FileNotFoundError(f"Image file not found at {image_path}")
        return None
    except OSError as e:
        logging.error(f"OS Error: {e}")
        # Removed redundant re-raise: raise OSError(f"OS Error: {e}")
        return None


# Run inference
def run_inference(image_path, confidence_threshold=0.1):
    if not os.path.exists(image_path):
        logging.error(f"Inference failed: Image file not found at {image_path}")
        return None

    logging.info(f"Running inference on image: {image_path}")
    image_path = os.path.abspath(image_path)

    python_executable = sys.executable  # Get the correct Python executable
    inference_script = BASE_DIR / "inference.py"  # Use absolute path to inference.py

    try:
        result = subprocess.run(
            [python_executable, str(inference_script), image_path, str(confidence_threshold)],
            capture_output=True, text=True, timeout=30
        )

        if result.returncode != 0:
            logging.error(f"Inference failed with return code {result.returncode}")
            logging.error(f"Error message: {result.stderr}")
            return None

        logging.info("Inference completed successfully.")
        return result.stdout

    except subprocess.TimeoutExpired:
        logging.error("Inference script timed out.")
        return None
    except Exception as e:
        logging.error(f"Unexpected error in inference: {e}")
        return None


# Ensure image_path is defined before running inference
def process_inference(image_path):
    raw_results = run_inference(image_path)
    if not raw_results:
        logging.error(f"Inference failed or returned no data for {image_path}.")
        return
    return raw_results


def parse_results(results):
    if not results:
        logging.warning("No inference results received.")
        return {}

    logging.info("Parsing inference results.")
    parsed_results = {}

    # Improved regex for robustness
    pattern = re.compile(r"([\w\s]+):\s*([\d.]+)%")

    for line in results.split("\n"):
        match = pattern.search(line)
        if match:
            label = match.group(1).strip()
            confidence = float(match.group(2)) / 100  # Convert % to decimal
            parsed_results[label] = confidence

    logging.info(f"Parsed results: {parsed_results}")
    return parsed_results


# Function to save predictions to database
def save_predictions_to_db(image_path, parsed_results):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if not parsed_results:
        logging.warning(f"No predictions found for {image_path}, skipping database update.")
        return

    set_clause = ", ".join([f"{key} = ?" for key in parsed_results.keys()])
    values = list(parsed_results.values()) + [image_path]

    sql_query = f"UPDATE detections SET {set_clause} WHERE image_path = ?"
    logging.info(f"Executing SQL: {sql_query} with values {values}")

    try:
        cursor.execute(sql_query, values)
        conn.commit()
        logging.info(f"Predictions saved to database for {image_path}: {parsed_results}")
    except sqlite3.Error as e:
        logging.error(f"Error updating database: {e}")
    finally:
        conn.close()


# Notifications
def notify_user(predictions, alert_threshold=0.3):
    logging.info("Checking predictions for notifications.")

    notification_triggered = "NO"  # Default to NO

    try:
        for label, confidence in predictions.items():
            if confidence > alert_threshold:
                logging.info(f"Triggering notification for: {label} with confidence: {confidence * 100:.2f}%")
                # Using subprocess on Windows to ensure notification is visible on desktop
                notification.notify(
                    title="Wrinkle Detection Alert",
                    message="You are frowning, try to relax your face",
                    timeout=5
                )
                notification_triggered = "YES"
            else:
                logging.info(f"No notification triggered for: {label} with confidence: {confidence * 100:.2f}%")
    except Exception as e:
        logging.error(f"Error in notification system: {e}")

    # Save notification status and threshold to the database
    save_notification_to_db(notification_triggered, alert_threshold)


def save_notification_to_db(notification_status, threshold):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            UPDATE detections 
            SET notification = ?, notification_threshold = ? 
            WHERE id = (SELECT MAX(id) FROM detections)
        ''', (notification_status, threshold))
        conn.commit()
        logging.info(f"Notification status '{notification_status}' and threshold '{threshold}' saved to database.")
    except sqlite3.Error as e:
        logging.error(f"Error updating database with notification status: {e}")
    finally:
        conn.close()

# Removed the original main() function to use the API-exposed functions instead
# def main():
#     ...

# if __name__ == "__main__":
#     main()
