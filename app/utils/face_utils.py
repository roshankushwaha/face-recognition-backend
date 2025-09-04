import cv2
import numpy as np
from PIL import Image
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.7)

def detect_and_crop_face(image_np: np.ndarray) -> tuple[np.ndarray, np.ndarray] | None:
    """
    Detects and crops a face from an image, resizes it to 160x160, returns normalized face and BGR face for saving.
    """

    try:
        print(f"🔍 Original image shape: {image_np.shape}")

        # Convert to RGB
        image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)

        # Face detection
        result = face_detection.process(image_rgb)

        if not result.detections:
            print("🚫 No face detected!")
            return None

        print(f"✅ {len(result.detections)} face(s) detected")

        # Bounding box
        bbox = result.detections[0].location_data.relative_bounding_box
        h, w, _ = image_rgb.shape
        x1 = int(bbox.xmin * w)
        y1 = int(bbox.ymin * h)
        x2 = x1 + int(bbox.width * w)
        y2 = y1 + int(bbox.height * h)

        print(f"📦 Bounding box: ({x1}, {y1}), ({x2}, {y2})")

        face = image_rgb[max(y1, 0):min(y2, h), max(x1, 0):min(x2, w)]

        if face.size == 0:
            print("⚠️ Cropped face has zero size.")
            return None

        print(f"🖼️ Cropped face shape: {face.shape}")

        # Resize to 160x160
        face_resized = Image.fromarray(face).resize((160, 160))
        face_resized_np = np.array(face_resized)

        # Normalize for model
        face_normalized = face_resized_np.astype("float32") / 255.0

        # For saving: convert RGB to BGR
        face_bgr = cv2.cvtColor(face_resized_np, cv2.COLOR_RGB2BGR)

        # return face_normalized, face_bgr
        return face_normalized

    except Exception as e:
        print("❌ Error during face detection:", str(e))
        return None


