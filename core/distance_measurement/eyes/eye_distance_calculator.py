# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/distance_measurement/eyes/eye_distance_calculator.py
import numpy as np
from abc import ABC, abstractmethod
from ..gesture_distance import process_eye_distances  # Importación correcta

# === Base de cálculo de distancia ===

class DistanceCalculator(ABC):
    @abstractmethod
    def calculate_distance(self, point1, point2):
        pass

class EuclideanDistanceCalculator(DistanceCalculator):
    def calculate_distance(self, point1, point2):
        point1 = np.array(point1)
        point2 = np.array(point2)
        return np.linalg.norm(point1 - point2)

# === Procesamiento de puntos de ojos ===

class EyesPointsProcessing:
    def __init__(self, distance_calculator: DistanceCalculator):
        self.distance_calculator = distance_calculator
        self.eyes: dict = {}

    def calculate_distances(self, eyes_points: dict):
        distances = eyes_points.get('distances', [])
        if len(distances) < 8:
            return None  # No hay suficientes puntos para procesar

        # Calculando las distancias entre los puntos de los párpados
        right_upper_eyelid = self.distance_calculator.calculate_distance(distances[0], distances[1])
        left_upper_eyelid = self.distance_calculator.calculate_distance(distances[2], distances[3])
        right_lower_eyelid = self.distance_calculator.calculate_distance(distances[4], distances[5])
        left_lower_eyelid = self.distance_calculator.calculate_distance(distances[6], distances[7])

        # Devolver las distancias como un diccionario
        return {
            'right_upper_eyelid_distance': right_upper_eyelid,
            'left_upper_eyelid_distance': left_upper_eyelid,
            'right_lower_eyelid_distance': right_lower_eyelid,
            'left_lower_eyelid_distance': left_lower_eyelid
        }

    def main(self, eyes_points: dict):
        # Calcular las distancias
        distances = self.calculate_distances(eyes_points)
        if distances:
            self.eyes.update(distances)
            # Enviar el diccionario de distancias a gesture_distance
            process_eye_distances(self.eyes)  # Pasamos el diccionario
        return self.eyes

# === Función principal que se invoca desde point_router ===

def receive_eye_points(points):
    processor = EyesPointsProcessing(EuclideanDistanceCalculator())
    distances = processor.main(points)
