# core/distance_measurement/hands/hand_to_face_distance.py

import numpy as np
from abc import ABC, abstractmethod
from ..gesture_distance import process_hand_distances  # Importar la función de procesamiento


# === Base para cálculo de distancias ===
class DistanceCalculator(ABC):
    @abstractmethod
    def calculate_distance(self, point1, point2):
        pass


class EuclideanDistanceCalculator(DistanceCalculator):
    def calculate_distance(self, point1, point2):
        return np.linalg.norm(np.array(point1) - np.array(point2))


# === Calculadora para distancias entre dedos y ojos ===
class FingerEyeDistanceCalculator:
    def __init__(self, distance_calculator: DistanceCalculator):
        self.distance_calculator = distance_calculator

    def calculate_finger_eye_distances(self, finger_points: list, eye_point: list) -> dict:
        return {
            'thumb': self.distance_calculator.calculate_distance(finger_points[0], eye_point),
            'index_finger': self.distance_calculator.calculate_distance(finger_points[1], eye_point),
            'middle_finger': self.distance_calculator.calculate_distance(finger_points[2], eye_point),
            'ring_finger': self.distance_calculator.calculate_distance(finger_points[3], eye_point),
            'little_finger': self.distance_calculator.calculate_distance(finger_points[4], eye_point),
        }


# === Procesamiento de la primera mano ===
class FirstHandPointsProcessing:
    def __init__(self, distance_calculator: DistanceCalculator):
        self.finger_eye_calculator = FingerEyeDistanceCalculator(distance_calculator)

    def main(self, hand_points: list, eyes_points: list) -> dict:
        hand_to_eyes_distances = {
            'hand_to_right_eye': self.finger_eye_calculator.calculate_finger_eye_distances(hand_points, eyes_points[8]),
            'hand_to_left_eye': self.finger_eye_calculator.calculate_finger_eye_distances(hand_points, eyes_points[9])
        }
        # Enviar distancias calculadas para procesamiento de gestos
        process_hand_distances(hand_to_eyes_distances)
        return hand_to_eyes_distances


# === Procesamiento de la segunda mano ===
class SecondHandPointsProcessing:
    def __init__(self, distance_calculator: DistanceCalculator):
        self.finger_eye_calculator = FingerEyeDistanceCalculator(distance_calculator)

    def main(self, hand_points: list, eyes_points: list) -> dict:
        hand_to_eyes_distances = {
            'hand_to_right_eye': self.finger_eye_calculator.calculate_finger_eye_distances(hand_points, eyes_points[8]),
            'hand_to_left_eye': self.finger_eye_calculator.calculate_finger_eye_distances(hand_points, eyes_points[9])
        }
        process_hand_distances(hand_to_eyes_distances)
        return hand_to_eyes_distances


# === Función principal llamada desde point_router ===
def receive_hand_and_eye_points(hands, eyes):
    if len(eyes) < 10:
        print("❌ No hay suficientes puntos de ojos para calcular distancias.")
        return

    calculator = EuclideanDistanceCalculator()

    # Procesar primera mano si existe
    if len(hands) > 0:
        first_hand_processor = FirstHandPointsProcessing(calculator)
        first_hand_processor.main(hands[0], eyes)

    # Procesar segunda mano si existe
    if len(hands) > 1:
        second_hand_processor = SecondHandPointsProcessing(calculator)
        second_hand_processor.main(hands[1], eyes)
