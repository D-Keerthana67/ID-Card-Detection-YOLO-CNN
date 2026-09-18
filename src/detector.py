from pathlib import Path

import cv2
from ultralytics import YOLO


class IDCardDetector:
    def __init__(self, model_path, confidence=0.5, person_class_id=0):
        self.confidence = confidence
        self.person_class_id = person_class_id
        if not Path(model_path).exists():
            raise FileNotFoundError(
                f"YOLO model not found: {model_path}. Place your trained model in models/."
            )
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model.predict(source=frame, conf=self.confidence, verbose=False)
        persons, id_cards = [], []
        if not results or results[0].boxes is None:
            return persons, id_cards

        result = results[0]
        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            class_name = str(result.names[class_id]).lower()

            if class_id == self.person_class_id or class_name == "person":
                persons.append((x1, y1, x2, y2, confidence))
            if "id" in class_name and "card" in class_name:
                id_cards.append((x1, y1, x2, y2, confidence))
        return persons, id_cards

    @staticmethod
    def draw_detections(frame, persons, id_cards):
        for x1, y1, x2, y2, confidence in persons:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
            cv2.putText(frame, f"Person {confidence:.2f}", (x1, max(y1 - 8, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        for x1, y1, x2, y2, confidence in id_cards:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
            cv2.putText(frame, f"ID Card {confidence:.2f}", (x1, max(y1 - 8, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        return frame
