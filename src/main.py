import cv2

try:
    import config
except ImportError as error:
    raise SystemExit("Create config.py from config.example.py before running.") from error

from detector import IDCardDetector
from email_alert import EmailAlert
from violation_manager import ViolationManager


def main():
    detector = IDCardDetector(config.YOLO_MODEL_PATH, config.YOLO_CONFIDENCE, config.PERSON_CLASS_ID)
    email_alert = EmailAlert(config.EMAIL_SENDER, config.EMAIL_PASSWORD,
                             config.EMAIL_RECEIVER, config.SMTP_SERVER, config.SMTP_PORT)
    manager = ViolationManager(config.WARNING_LIMIT, config.FINE_AMOUNT, config.FINE_LOG_PATH)

    camera = cv2.VideoCapture(config.CAMERA_INDEX)
    if not camera.isOpened():
        raise SystemExit("Unable to open the camera.")

    missing_frames = 0
    print("ID Card Detection started. Press Q to exit.")

    while True:
        success, frame = camera.read()
        if not success:
            break

        persons, id_cards = detector.detect(frame)
        violation = len(persons) > 0 and len(id_cards) == 0
        missing_frames = missing_frames + 1 if violation else 0

        if missing_frames >= config.VIOLATION_CONFIRMATION_FRAMES:
            action, value = manager.register_violation(config.STUDENT_ID)
            if action == "warning":
                try:
                    email_alert.send_warning(config.STUDENT_ID, value)
                    print(f"Warning {value} email sent.")
                except Exception as error:
                    print(f"Email could not be sent: {error}")
            else:
                print(f"Fine recorded for {config.STUDENT_ID}: Rs. {value}")
            missing_frames = 0

        frame = detector.draw_detections(frame, persons, id_cards)
        status = "COMPLIANT" if id_cards else "CHECK ID CARD"
        cv2.putText(frame, status, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow("ID Card Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
