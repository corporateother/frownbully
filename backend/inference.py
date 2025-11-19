import sys
import base64
from inference_sdk import InferenceHTTPClient

# ✅ Read command-line arguments
if len(sys.argv) > 2:
    image_path = sys.argv[1]
    threshold = float(sys.argv[2])
else:
    image_path = input("Enter image path: ")
    threshold = float(input("Enter confidence threshold (e.g., 0.5 for 50%): "))

# ✅ Convert Image to Base64
def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        print("Error: Image file not found.")
        sys.exit(1)

# Initialize Roboflow client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="RuaSyrBdxkwItfFCT4cr"
)

# ✅ Send Base64 Image to Roboflow API
encoded_image = encode_image(image_path)
result = CLIENT.infer(encoded_image, model_id="wrinkle-detection/2")

# ✅ Extract predictions
predictions = result.get("predictions", [])

# ✅ Filter Predictions
filtered_classes = [
    (pred["class"], pred["confidence"])
    for pred in predictions if pred["confidence"] >= threshold
]

# ✅ Print Results
if filtered_classes:
    print("\n### Detected Wrinkle Types ###")
    for label, confidence in filtered_classes:
        print(f"{label}: {confidence:.2%} confidence")
else:
    print("\nNo wrinkles detected above the threshold.")

