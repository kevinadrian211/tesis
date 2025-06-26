# core/distance_measurement/head/head_movement_calculator.py
import numpy as np
from abc import ABC, abstractmethod
from ..gesture_distance import process_head_distances  # Importar la función

class DistanceCalculator(ABC):
    @abstractmethod
    def calculate_distance(self, point1, point2):
        pass

class EuclideanDistanceCalculator(DistanceCalculator):
    def calculate_distance(self, point1, point2):
        return np.linalg.norm(np.array(point1) - np.array(point2))


def average_point(points):
    points_array = np.array(points)
    return points_array.mean(axis=0)


class HeadPointsProcessing:
    def __init__(self, distance_calculator: DistanceCalculator):
        self.distance_calculator = distance_calculator
        self.head: dict = {}

    def calculate_distances(self, forehead_points: list, nose_points: list, mouth_points: list):
        forehead_point = average_point(forehead_points)
        nose_point = average_point(nose_points)
        mouth_point = average_point(mouth_points)

        forehead_to_nose = self.distance_calculator.calculate_distance(forehead_point, nose_point)
        nose_to_mouth = self.distance_calculator.calculate_distance(nose_point, mouth_point)
        forehead_to_mouth = self.distance_calculator.calculate_distance(forehead_point, mouth_point)

        return forehead_to_nose, nose_to_mouth, forehead_to_mouth

    def main(self, forehead_points: list, nose_points: list, mouth_points: list):
        forehead_to_nose_distance, nose_to_mouth_distance, forehead_to_mouth_distance = self.calculate_distances(
            forehead_points, nose_points, mouth_points)

        self.head['forehead_to_nose_distance'] = forehead_to_nose_distance
        self.head['nose_to_mouth_distance'] = nose_to_mouth_distance
        self.head['forehead_to_mouth_distance'] = forehead_to_mouth_distance

        # Enviar las distancias a gesture_distance.py
        process_head_distances(self.head)  # Pasamos el diccionario con las distancias de la cabeza
        return self.head


# Función para recibir los puntos y hacer el cálculo
def receive_head_points(forehead, nose, mouth):

    processor = HeadPointsProcessing(EuclideanDistanceCalculator())
    distances = processor.main(forehead, nose, mouth)
    return distances
