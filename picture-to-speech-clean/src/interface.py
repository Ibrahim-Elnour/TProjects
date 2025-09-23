from typing import Dict
import cv2
import numpy as np
from .recognition import classify

def run_camera_loop(bank: Dict[str, np.ndarray], speaker, confidence_threshold: float = 0.60) -> None:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")
    msg = "SPACE: classify | t: type text | q: quit"
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        cv2.putText(frame, msg, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.imshow("Picture to Speech", frame)
        key = cv2.waitKey(10) & 0xFF
        if key == ord("q"):
            break
        elif key == ord(" "):
            label, score = classify(frame, bank)
            out = f"{label} ({score:.2f})"
            color = (0, 255, 0) if score >= confidence_threshold else (0, 0, 255)
            echo = label if score >= confidence_threshold else "I did not understand"
            info = frame.copy()
            cv2.putText(info, out, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            cv2.imshow("Picture to Speech", info)
            cv2.waitKey(300)
            speaker.speak(echo)
        elif key == ord("t"):
            try:
                text = input("\nType phrase to speak: ").strip()
            except EOFError:
                text = ""
            if text:
                speaker.speak(text)
    cap.release()
    cv2.destroyAllWindows()
