# core/pose_extraction/point_router.py

from distance_measurement.eyes.eye_distance_calculator import receive_eye_points
from distance_measurement.hands.hand_to_face_distance import receive_hand_and_eye_points
from distance_measurement.head.head_movement_calculator import receive_head_points
from distance_measurement.mouth.mouth_distance_calculator import receive_mouth_points


def send_face_points_to_router(points: dict):

    # 👁️ Ojos: Enviar a ojos y también a manos
    eye_points = points.get("eyes", {})  # Ojo, aquí quitamos .get('distances', [])
    receive_eye_points(eye_points)  # Ojos
    send_eye_points_to_hand_module(eye_points)  # Para usar junto con manos

    # 🔵 Frente, 👃 Nariz, 🧔 Mentón: Enviar directamente
    forehead_points = points.get("forehead", {}).get("distances", [])
    nose_points = points.get("nose", {}).get("distances", [])
    chin_points = points.get("chin", {}).get("distances", [])
    receive_head_points(forehead_points, nose_points, chin_points)

    # 👄 Boca: Enviar directamente
    mouth_points = points.get("mouth", {}).get("distances", [])
    receive_mouth_points(mouth_points)


# Guarda temporalmente los últimos puntos de ojos para enviarlos junto con manos
_last_eye_points = []


def send_eye_points_to_hand_module(eye_points: dict):
    global _last_eye_points
    _last_eye_points = eye_points.get("distances", [])



def send_hand_points_to_router(points: dict):
    hands = points.get('hands', [])
    receive_hand_and_eye_points(hands, _last_eye_points)
