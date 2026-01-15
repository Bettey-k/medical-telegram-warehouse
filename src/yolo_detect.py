import os
import pandas as pd
from ultralytics import YOLO
from tqdm import tqdm

# -----------------------
# Configuration
# -----------------------
IMAGE_DIR = "data/raw/images"
OUTPUT_CSV = "data/yolo_detections.csv"
MODEL_NAME = "yolov8n.pt"

# -----------------------
# Load YOLO model
# -----------------------
model = YOLO(MODEL_NAME)

results = []

# -----------------------
# Walk through image folders
# -----------------------
for root, _, files in os.walk(IMAGE_DIR):
    for file in tqdm(files, desc="Processing images"):
        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        try:
            # filename = message_id (e.g. 22820.jpg)
            message_id = int(os.path.splitext(file)[0])
        except ValueError:
            continue

        image_path = os.path.join(root, file)

        yolo_result = model(image_path)[0]

        detected_objects = []
        confidences = []

        for box in yolo_result.boxes:
            cls_name = model.names[int(box.cls)]
            conf = float(box.conf)

            detected_objects.append(cls_name)
            confidences.append(conf)

        has_person = "person" in detected_objects
        has_product = any(obj in ["bottle", "cup", "container"] for obj in detected_objects)

        if has_person and has_product:
            image_category = "promotional"
        elif has_product and not has_person:
            image_category = "product_display"
        elif has_person and not has_product:
            image_category = "lifestyle"
        else:
            image_category = "other"

        results.append({
            "message_id": message_id,
            "detected_objects": ",".join(detected_objects),
            "avg_confidence": round(sum(confidences) / len(confidences), 3) if confidences else 0,
            "image_category": image_category
        })

# -----------------------
# Save results
# -----------------------
df = pd.DataFrame(results)
df.to_csv(OUTPUT_CSV, index=False)

print(f"✅ YOLO detection finished. Saved {len(df)} rows to {OUTPUT_CSV}")
