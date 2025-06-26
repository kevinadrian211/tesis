# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/gesture_detection/nods/nod_detector.py
import time
from ..gestures import receive_nod_gesture  # Importa la función para recibir el gesto

# Umbrales ajustados según los rangos observados
DISTANCE_THRESHOLD_FOREHEAD_NOSE = 10.0
DISTANCE_THRESHOLD_NOSE_MOUTH = 50.0

class PitchDetection:
    def __init__(self):
        self.start_time = 0
        self.flag = False

    def check_head_down(self, head_distances: dict) -> bool:
        forehead_to_nose_distance = head_distances.get('forehead_to_nose_distance', None)
        nose_to_mouth_distance = head_distances.get('nose_to_mouth_distance', None)

        if forehead_to_nose_distance is None or nose_to_mouth_distance is None:
            return False

        return (forehead_to_nose_distance < DISTANCE_THRESHOLD_FOREHEAD_NOSE and
                nose_to_mouth_distance < DISTANCE_THRESHOLD_NOSE_MOUTH)

    def detect(self, head_down: bool) -> bool:
        if head_down and not self.flag:
            self.start_time = time.time()
            self.flag = True
        elif not head_down and self.flag:
            pitch_duration = time.time() - self.start_time
            self.flag = False
            if pitch_duration >= 0:
                self.start_time = 0
                return True
        return False

pitch_detector = PitchDetection()

def receive_head_distances(head_distances: dict):
    head_down = pitch_detector.check_head_down(head_distances)
    if pitch_detector.detect(head_down):
        # Enviar detección a gestures.py en lugar de imprimir
        receive_nod_gesture(duration=None)  # Puedes pasar duración o cualquier info extra si quieres
