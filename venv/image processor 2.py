import cv2
import time
import subprocess
import logging
import os
import base64
import re
import sys
from datetime import datetime
from plyer import notification

# Generate a unique log file with timestamp
log_filename = f"script_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

#image capturing
def capture_image(image_path="captured_image.jpg", max_retries=3):
    image_path = os.path.normpath(image_path)  # ✅ Correct placement
    logging.info("Capturing image from webcam.")
    cap = cv2.VideoCapture(0)

    for attempt in range(max_retries):
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(image_path, frame)
            logging.info(f"Image captured successfully: {image_path}")
            cap.release()
            return image_path
        else:
            logging.warning(f"Attempt {attempt + 1}: Failed to capture image. Retrying...")
            time.sleep(1)

    logging.error("Failed to capture image after multiple attempts.")
    cap.release()
    return None

# ✅ Ensure the path is correctly formatted
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

# run iference
def run_inference(image_path, confidence_threshold=0.3):
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


def notify_user(predictions, alert_threshold=0.5):
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
            time.sleep(5)  # Capture image every 5s
            image_path = capture_image()
            if not image_path:
                continue  # Skip to next loop iteration if capture fails

            raw_results = run_inference(image_path)
            if raw_results is None:
                continue  # Skip to next loop iteration if inference fails

            parsed_results = parse_results(raw_results)
            notify_user(parsed_results)

    except KeyboardInterrupt:
        logging.info("Script terminated by user.")

if __name__ == "__main__":
    main()

