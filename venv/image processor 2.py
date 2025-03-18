import cv2
import time
import subprocess
import logging
import os
import base64
import re
import sys
import sqlite3
from datetime import datetime
from plyer import notification

# Generate a unique log file with timestamp
log_filename = f"script_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


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

            return image_path
        else:
            logging.warning(f"Attempt {attempt + 1}: Failed to capture image. Retrying...")
            time.sleep(1)

        captured_image_path = capture_image()

        if captured_image_path and not os.path.exists(captured_image_path):
            logging.error(f"Image not found at: {captured_image_path}")

    logging.error("Failed to capture image after multiple attempts.")
    cap.release()
    return None


# Function to save image path in the database
def save_image_to_db(image_path):
    conn = sqlite3.connect("wrinkle_detection.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO detections (image_path) VALUES (?)
    ''', (image_path,))

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
        raise FileNotFoundError(f"Image file not found at {image_path}")
    except OSError as e:
        logging.error(f"OS Error: {e}")
        raise OSError(f"OS Error: {e}") #why am i doing this??

# Run inference
def run_inference(image_path, confidence_threshold=0.1):
    if not os.path.exists(image_path):
        logging.error(f"Inference failed: Image file not found at {image_path}")
        return None

    logging.info(f"Running inference on image: {image_path}")
    image_path = os.path.abspath(image_path)

    python_executable = sys.executable  # Get the correct Python executable

    try:
        result = subprocess.run(
            [python_executable, "inference.py", image_path, str(confidence_threshold)],
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
        return  # Use return instead of continue if not inside a loop
    return raw_results  # Process raw results further if needed


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
    conn = sqlite3.connect("wrinkle_detection.db")
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


#Notifications
def notify_user(predictions, alert_threshold=0.3):
    logging.info("Checking predictions for notifications.")

    try:
        for label, confidence in predictions.items():
            if confidence > alert_threshold:
                logging.info(f"Triggering notification for: {label} with confidence: {confidence * 100:.2f}%")
                notification.notify(
                    title="Wrinkle Detection Alert",
                    message="You are frowning, try to relax your face",
                    timeout=5
                )
            else:
                logging.info(f"No notification triggered for: {label} with confidence: {confidence * 100:.2f}%")
    except Exception as e:
        logging.error(f"Error in notification system: {e}")


def main():
    logging.info("Starting the script.")
    try:
        while True:
            time.sleep(1)  # Capture image every 1s
            image_path = capture_image()
            if not image_path:
                continue  # Skip to next loop iteration if capture fails

            raw_results = run_inference(image_path)
            if raw_results is None:
                continue  # Skip to next loop iteration if inference fails

            parsed_results = parse_results(raw_results)
            if parsed_results:
                save_predictions_to_db(image_path, parsed_results)
            else:
                logging.warning(f"No predictions found for {image_path}, skipping database update.")

            notify_user(parsed_results)

    except KeyboardInterrupt:
        logging.info("Script terminated by user.")

if __name__ == "__main__":
    main()

