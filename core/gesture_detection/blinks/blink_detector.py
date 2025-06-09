# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/gesture_detection/blinks/blink_detector.py
import time
from gesture_detection.gestures import receive_blink_gesture, receive_microsleep_gesture

class BlinkAndMicroSleepDetector:
    def __init__(self):
        # Estado de si ambos ojos están cerrados
        self.both_eyes_closed = False
        # Tiempo en el que ambos ojos se cierran
        self.eyes_start_time = 0
        # Umbral para considerar que el ojo está cerrado
        self.CLOSED_THRESHOLD = 1.0

    def process_eye_distances(self, eye_distances: dict):
        current_time = time.time()

        # Obtener las distancias de los párpados de cada ojo
        right_upper = eye_distances.get('right_upper_eyelid_distance')
        right_lower = eye_distances.get('right_lower_eyelid_distance')
        left_upper = eye_distances.get('left_upper_eyelid_distance')
        left_lower = eye_distances.get('left_lower_eyelid_distance')

        # Verificar que todas las distancias estén presentes
        if None in (right_upper, right_lower, left_upper, left_lower):
            return

        # Determinar si cada ojo está cerrado
        right_eye_closed_now = right_upper - right_lower < self.CLOSED_THRESHOLD
        left_eye_closed_now = left_upper - left_lower < self.CLOSED_THRESHOLD
        both_eyes_closed_now = right_eye_closed_now and left_eye_closed_now

        # Inicia el conteo cuando ambos ojos se cierran
        if both_eyes_closed_now and not self.both_eyes_closed:
            self.both_eyes_closed = True
            self.eyes_start_time = current_time

        # Cuando se abren después de estar cerrados
        elif not both_eyes_closed_now and self.both_eyes_closed:
            duration = (current_time - self.eyes_start_time) * 1000  # ms

            # Solo procesar el gesto si ambos ojos estuvieron cerrados
            if self.both_eyes_closed:
                if duration >= 1000:
                    # Llamar a la función para microsueño
                    receive_microsleep_gesture("ambos Ojos", duration)
                else:
                    # Llamar a la función para parpadeo
                    receive_blink_gesture("ambos Ojos", duration)

            # Resetear el estado de 'both_eyes_closed' después de procesar el gesto
            self.both_eyes_closed = False

# Instancia global del detector
detector = BlinkAndMicroSleepDetector()

def receive_eye_distances(eye_distances: dict):
    """
    Función que recibe las distancias de los párpados de los ojos
    y las pasa al detector para su procesamiento.
    """
    detector.process_eye_distances(eye_distances)
