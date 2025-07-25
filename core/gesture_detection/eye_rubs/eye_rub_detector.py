from ..gestures import receive_eye_rub_gesture
import time
from collections import deque

THRESHOLD_DISTANCE = 350  # Umbral para determinar si una mano está cerca del ojo
MIN_VALID_FINGERS = 3     # Número mínimo de dedos válidos para procesar
SMOOTHING_FRAMES = 5      # Cuántos frames promediar para suavizar la detección
GESTURE_MIN_DURATION = 1  # Duración mínima del gesto (en segundos)

class EyeRubDetection:
    def __init__(self, threshold=THRESHOLD_DISTANCE):
        self.start_time = 0
        self.flag = False
        self.threshold = threshold
        self.history = deque(maxlen=SMOOTHING_FRAMES)

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

        # Si hay muy pocos dedos válidos, ignorar este frame
        if len(valid_distances) < MIN_VALID_FINGERS:
            return False

        avg_distance = sum(valid_distances) / len(valid_distances)
        self.history.append(avg_distance)

        # Suavizado temporal con histórico
        smoothed_avg = sum(self.history) / len(self.history)
        close = smoothed_avg < self.threshold
        return close

    def detect(self, eye_rub: bool) -> bool:
        current_time = time.time()

        if eye_rub and not self.flag:
            self.start_time = current_time
            self.flag = True
            return False

        elif not eye_rub and self.flag:
            duration = current_time - self.start_time
            self.flag = False
            if duration >= GESTURE_MIN_DURATION:
                return True

        return False

# Instancia global del detector
detector = EyeRubDetection()

# Reservado si más adelante se quiere hacer algo con distancias de ojos directamente
def receive_eye_distances(eye_distances: dict):
    pass

# Llamado externo con las distancias mano-ojo
def receive_hand_distances(hand_distances: dict):
    for hand_eye, fingers_distances in hand_distances.items():
        if not isinstance(fingers_distances, dict):
            continue

        eye_rub = detector.check_eye_rub(fingers_distances)

        if detector.detect(eye_rub):
            receive_eye_rub_gesture()  # Enviamos señal
