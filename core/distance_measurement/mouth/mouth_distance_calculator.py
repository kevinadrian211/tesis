# core/distance_measurement/mouth/mouth_distance_calculator.py

import numpy as np
from abc import ABC, abstractmethod
from ..gesture_distance import process_mouth_distances


# Abstract base class for distance calculation
class DistanceCalculator(ABC):
    @abstractmethod
    def calculate_distance(self, point1, point2) -> float:
        pass


# Concrete implementation using Euclidean distance
class EuclideanDistanceCalculator(DistanceCalculator):
    def calculate_distance(self, point1, point2) -> float:
        return np.linalg.norm(np.array(point1) - np.array(point2))


class MouthDistanceProcessor:
    def __init__(self, calculator: DistanceCalculator):
        self.calculator = calculator

    def _calculate_distances(self, mouth_points: list) -> dict:
        if len(mouth_points) < 4:
            raise ValueError("Se requieren al menos 4 puntos para calcular las distancias de labios y mentón.")

        lips_distance = self.calculator.calculate_distance(mouth_points[0], mouth_points[1])
        chin_distance = self.calculator.calculate_distance(mouth_points[2], mouth_points[3])

        return {
            'lips_distance': lips_distance,
            'chin_distance': chin_distance,
        }

    def process(self, mouth_points: list) -> dict:
        distances = self._calculate_distances(mouth_points)
        process_mouth_distances(distances)
        return distances


def receive_mouth_points(mouth: list) -> dict:
    processor = MouthDistanceProcessor(EuclideanDistanceCalculator())
    return processor.process(mouth)
