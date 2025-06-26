# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/gesture_detection/eye_rubs/eye_rub_detector.py
from ..gestures import receive_eye_rub_gesture
import time

THRESHOLD_DISTANCE = 350

class EyeRubDetection:
    def __init__(self, threshold=THRESHOLD_DISTANCE):
        self.start_time = 0
        self.flag = False
        self.threshold = threshold

    def check_eye_rub(self, fingers_distances: dict) -> bool:
        distances = []
        for finger in ['thumb', 'index_finger', 'middle_finger', 'ring_finger', 'little_finger']:
            dist = fingers_distances.get(finger, float('inf'))
            try:
                dist = float(dist)
            except (TypeError, ValueError):
                dist = float('inf')
            distances.append(dist)

        valid_distances = [d for d in distances if d != float('inf')]
        avg_distance = sum(valid_distances) / len(valid_distances) if valid_distances else float('inf')

        close = avg_distance < self.threshold
        return close

    def detect(self, eye_rub: bool) -> bool:
        if eye_rub and not self.flag:
            self.start_time = time.time()
            self.flag = True
            return False
        elif not eye_rub and self.flag:
            duration = time.time() - self.start_time
            self.flag = False
            if duration > 1:
                return True
        return False

detector = EyeRubDetection()

def receive_eye_distances(eye_distances: dict):
    # Por ahora vacío, depende de si necesitas implementarlo
    pass

def receive_hand_distances(hand_distances: dict):
    for hand_eye, fingers_distances in hand_distances.items():
        if not isinstance(fingers_distances, dict):
            continue
        eye_rub = detector.check_eye_rub(fingers_distances)
        if detector.detect(eye_rub):
            receive_eye_rub_gesture()  # Enviamos señal
 