import time
from ..gestures import receive_nod_gesture  # Función para enviar la señal del gesto

# Umbrales para determinar inclinación de cabeza hacia abajo
THRESHOLD_FOREHEAD_NOSE = 10.0
THRESHOLD_NOSE_MOUTH = 50.0

# Duración mínima del gesto (en segundos)
MIN_NOD_DURATION = 0.3

class PitchDetection:
    def __init__(self):
        self.start_time = 0
        self.flag = False

    def check_head_down(self, head_distances: dict) -> bool:
        """Evalúa si la cabeza está inclinada hacia abajo según distancias clave"""
        forehead_to_nose = head_distances.get('forehead_to_nose_distance')
        nose_to_mouth = head_distances.get('nose_to_mouth_distance')

        # Validaciones de entrada
        if forehead_to_nose is None or nose_to_mouth is None:
            return False

        # Retorna True si la cabeza parece inclinada
        return (
            forehead_to_nose < THRESHOLD_FOREHEAD_NOSE and
            nose_to_mouth < THRESHOLD_NOSE_MOUTH
        )

    def detect(self, head_down: bool) -> bool:
        """Detecta un gesto de asentir cabeza (nod)"""
        current_time = time.time()

        if head_down and not self.flag:
            self.start_time = current_time
            self.flag = True

        elif not head_down and self.flag:
            duration = current_time - self.start_time
            self.flag = False
            self.start_time = 0

            # Validar duración mínima
            if duration >= MIN_NOD_DURATION:
                return True

        return False

# Instancia global del detector
pitch_detector = PitchDetection()

def receive_head_distances(head_distances: dict):
    """Recibe distancias de la cabeza desde el pipeline de detección"""
    head_down = pitch_detector.check_head_down(head_distances)

    if pitch_detector.detect(head_down):
        # Si deseas pasar duración o más datos, puedes modificar esta parte
        receive_nod_gesture(duration=None)
