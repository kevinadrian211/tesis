# core/pose_extraction/point_router.py

from ..distance_measurement.eyes.eye_distance_calculator import receive_eye_points
from ..distance_measurement.hands.hand_to_face_distance import receive_hand_and_eye_points
from ..distance_measurement.head.head_movement_calculator import receive_head_points
from ..distance_measurement.mouth.mouth_distance_calculator import receive_mouth_points


# Variable global para almacenar temporalmente los últimos puntos de ojos,
# que luego serán usados para combinarlos con las manos
_last_eye_points = []


def send_face_points_to_router(points: dict):
    """
    Recibe un diccionario con puntos del rostro y enruta
    cada conjunto de puntos a su respectivo módulo.
    """
    # Ojos
    eye_points = points.get("eyes", {})
    receive_eye_points(eye_points)
    send_eye_points_to_hand_module(eye_points)

    # Frente, nariz y mentón
    forehead_points = points.get("forehead", {}).get("distances", [])
    nose_points = points.get("nose", {}).get("distances", [])
    chin_points = points.get("chin", {}).get("distances", [])
    receive_head_points(forehead_points, nose_points, chin_points)

    # Boca
    mouth_points = points.get("mouth", {}).get("distances", [])
    receive_mouth_points(mouth_points)


def send_eye_points_to_hand_module(eye_points: dict):
    """
    Guarda temporalmente los puntos de ojos para combinarlos con
    puntos de manos en el cálculo de distancias.
    """
    global _last_eye_points
    _last_eye_points = eye_points.get("distances", [])


def send_hand_points_to_router(points: dict):
    """
    Recibe un diccionario con puntos de las manos y los envía junto
    con los últimos puntos de ojos registrados para su procesamiento conjunto.
    """
    hands = points.get('hands', [])
    receive_hand_and_eye_points(hands, _last_eye_points)
