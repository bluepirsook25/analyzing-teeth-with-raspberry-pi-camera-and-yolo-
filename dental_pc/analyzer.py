"""
analyzer.py  ──  YOLOv8 Nano Segmentation  •  PIL + Numpy only  •  No OpenCV
"""

from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
import config

MASK_COLORS = [
    (255, 56,  56),
    ( 56, 255,  56),
    ( 56,  56, 255),
    (255, 255,  56),
    (255,  56, 255),
    ( 56, 255, 255),
]

def _calculate_histogram(image_path: str) -> np.ndarray:
    img = Image.open(image_path).convert("RGB").resize((100, 100))
    arr = np.array(img, dtype=np.uint8)
    hists = []
    for ch in range(3):
        h, _ = np.histogram(arr[:, :, ch].flatten(), bins=256, range=(0, 256))
        hists.append(h)
    return np.concatenate(hists)

def _annotate_and_save(image_path: str, results, out_path: str) -> None:
    img     = Image.open(image_path).convert("RGB")
    overlay = img.copy()
    draw_ov = ImageDraw.Draw(overlay)

    result = results[0]

    if result.masks is not None:
        for idx, polygon in enumerate(result.masks.xy):
            if len(polygon) < 3:
                continue
            color = MASK_COLORS[idx % len(MASK_COLORS)]
            pts   = [tuple(p) for p in polygon.astype(int)]
            draw_ov.polygon(pts, fill=(*color, 140))
        img = Image.blend(img, overlay, alpha=0.45)

    draw_img = ImageDraw.Draw(img)

    if result.boxes is not None and len(result.boxes) > 0:
        boxes = result.boxes.xyxy.numpy().astype(int)
        confs = result.boxes.conf.numpy()
        clss  = result.boxes.cls.numpy().astype(int)
        try:
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14
            )
        except Exception:
            font = ImageFont.load_default()

        for (x1, y1, x2, y2), conf, cls_id in zip(boxes, confs, clss):
            color = MASK_COLORS[cls_id % len(MASK_COLORS)]
            label = f"cls{cls_id}  {conf:.2f}"
            for t in range(3):
                draw_img.rectangle(
                    [x1 - t, y1 - t, x2 + t, y2 + t], outline=color
                )
            bbox_txt = draw_img.textbbox((x1, y1 - 18), label, font=font)
            draw_img.rectangle(bbox_txt, fill=color)
            draw_img.text((x1, y1 - 18), label, fill="white", font=font)

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    img.save(out_path)
    print(f"🖼️  Annotated image → {out_path}")


def analyze_teeth():
    if not os.path.exists(config.ORIGINAL_IMAGE):
        return None, "Missing original_teeth.jpg in data/"
    if not os.path.exists(config.CAPTURED_IMAGE):
        return None, "Missing captured_teeth.jpg in data/"

    os.makedirs("models", exist_ok=True)
    if not os.path.exists(config.MODEL_PATH):
        print("⬇️  Downloading yolov8n-seg.pt …")
        model = YOLO("yolov8n-seg.pt")
        model.save(config.MODEL_PATH)
    else:
        model = YOLO(config.MODEL_PATH)
    print(f"✅ YOLOv8n-seg loaded from {config.MODEL_PATH}")

    print("🎨 Comparing colour histograms …")
    color_score = float(
        np.corrcoef(
            _calculate_histogram(config.ORIGINAL_IMAGE),
            _calculate_histogram(config.CAPTURED_IMAGE),
        )[0, 1]
    )

    print("🦷 Running YOLOv8n-seg inference …")
    results = model(config.CAPTURED_IMAGE, verbose=False, conf=0.25, iou=0.45)

    boxes = results[0].boxes
    masks = results[0].masks
    num_det   = len(boxes) if boxes is not None else 0
    mean_conf = float(boxes.conf.numpy().mean()) if num_det > 0 else 0.0
    num_masks = len(masks.xy) if masks is not None else 0

    _annotate_and_save(config.CAPTURED_IMAGE, results, config.ANNOTATED_IMAGE)

    issue_type = None
    if color_score < config.COLOR_THRESHOLD:
        issue_type = "color"
    elif mean_conf < config.STRUCTURE_THRESHOLD:
        issue_type = "edge"

    detail = (
        f"Color Score: {color_score:.2f} | "
        f"Mean Conf: {mean_conf:.2f} | "
        f"Detections: {num_det} | Masks: {num_masks}"
    )
    return issue_type, detail
