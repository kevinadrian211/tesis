# core/gesture_detection/blinks/blink_detector.py

import time
from ..gestures import receive_blink_gesture, receive_microsleep_gesture


class BlinkAndMicrosleepDetector:
    def __init__(self, closed_threshold: float = 1.0, microsleep_ms: int = 1000):
        self.closed_threshold = closed_threshold
        self.microsleep_ms = microsleep_ms

        self.both_eyes_closed = False
        self.eyes_start_time = 0.0

    def _eyes_closed(self, upper: float, lower: float) -> bool:
        return (upper - lower) < self.closed_threshold

    def process_eye_distances(self, eye_distances: dict):
        """
        Procesa las distancias de los párpados y determina si se ha producido un parpadeo o microsueño.
        """
        current_time = time.time()

        try:
            right_upper = eye_distances['right_upper_eyelid_distance']
            right_lower = eye_distances['right_lower_eyelid_distance']
            left_upper = eye_distances['left_upper_eyelid_distance']
            left_lower = eye_distances['left_lower_eyelid_distance']
        except KeyError:
            # Si falta alguna clave, no se puede procesar
            return

        right_closed = self._eyes_closed(right_upper, right_lower)
        left_closed = self._eyes_closed(left_upper, left_lower)
        both_closed_now = right_closed and left_closed

        if both_closed_now and not self.both_eyes_closed:
            # Inicio de cierre de ojos
            self.both_eyes_closed = True
            self.eyes_start_time = current_time

        elif not both_closed_now and self.both_eyes_closed:
            # Fin del cierre de ojos
            duration_ms = (current_time - self.eyes_start_time) * 1000

            if duration_ms >= self.microsleep_ms:
                receive_microsleep_gesture(duration_ms)
            else:
                receive_blink_gesture(duration_ms)

            self.both_eyes_closed = False


# Instancia global del detector
_detector = BlinkAndMicrosleepDetector()

def receive_eye_distances(eye_distances: dict):
    """
    Recibe las distancias de los párpados y las envía al detector para análisis.
    """
    _detector.process_eye_distances(eye_distances)
