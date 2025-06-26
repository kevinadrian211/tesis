# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/gesture_detection/yawns/yawn_detector.py
import time
from ..gestures import receive_yawn_gesture  # Importa la función para recibir el gesto

breathe_start_time = None
is_breathing_open = False  # Estado de la boca (abierta o cerrada)
flag = False  # Controla si estamos midiendo un gesto abierto

def receive_mouth_distances(mouth_distances: dict):
    global breathe_start_time, is_breathing_open, flag

    lips_distance = mouth_distances.get('lips_distance')
    chin_distance = mouth_distances.get('chin_distance')

    if lips_distance is None or chin_distance is None:
        return  # Sin datos suficientes

    open_mouth = lips_distance > chin_distance

    if open_mouth and not flag:
        # Boca se abre, iniciamos temporizador
        breathe_start_time = time.time()
        flag = True
        is_breathing_open = True

    elif not open_mouth and flag:
        # Boca se cierra, calculamos duración
        duration = time.time() - breathe_start_time
        flag = False
        is_breathing_open = False

        if 1 <= duration <= 7:
            # Enviar detección a gestures.py
            receive_yawn_gesture(duration)

        # Reiniciamos para detectar nuevos bostezos
        breathe_start_time = None
