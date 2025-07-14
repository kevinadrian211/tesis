import time
from ..gestures import receive_yawn_gesture

# Umbral de duración para considerar un bostezo (en segundos)
MIN_YAWN_DURATION = 1.0
MAX_YAWN_DURATION = 7.0

class YawnDetector:
    def __init__(self):
        self.start_time = None
        self.mouth_open = False

    def is_valid_number(self, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def check_mouth_open(self, lips_distance, chin_distance) -> bool:
        # Boca se considera abierta si la distancia entre labios es mayor que con el mentón
        return lips_distance > chin_distance

    def update(self, mouth_distances: dict):
        lips_distance = self.is_valid_number(mouth_distances.get('lips_distance'))
        chin_distance = self.is_valid_number(mouth_distances.get('chin_distance'))

        if lips_distance is None or chin_distance is None:
            return  # Datos no válidos

        mouth_open = self.check_mouth_open(lips_distance, chin_distance)

        current_time = time.time()

        if mouth_open and not self.mouth_open:
            # Boca se abre
            self.start_time = current_time
            self.mouth_open = True

        elif not mouth_open and self.mouth_open:
            # Boca se cierra
            duration = current_time - self.start_time
            self.mouth_open = False
            self.start_time = None

            if MIN_YAWN_DURATION <= duration <= MAX_YAWN_DURATION:
                receive_yawn_gesture(duration=duration)

# Instancia global
yawn_detector = YawnDetector()

def receive_mouth_distances(mouth_distances: dict):
    yawn_detector.update(mouth_distances)
