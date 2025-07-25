# core/distance_measurement/head/head_movement_calculator.py

import numpy as np
from abc import ABC, abstractmethod
from ..gesture_distance import process_head_distances


# Abstract base class for distance calculation
class DistanceCalculator(ABC):
    @abstractmethod
    def calculate_distance(self, point1, point2) -> float:
        pass


# Concrete implementation using Euclidean distance
class EuclideanDistanceCalculator(DistanceCalculator):
    def calculate_distance(self, point1, point2) -> float:
        point1, point2 = np.array(point1), np.array(point2)
        return np.linalg.norm(point1 - point2)


# Utility function to compute the average of a list of points
def average_point(points: list) -> np.ndarray:
    return np.mean(points, axis=0)


class HeadDistanceProcessor:
    def __init__(self, calculator: DistanceCalculator):
        self.calculator = calculator

    def _average_face_points(self, face_points: dict) -> dict:
        return {
            region: average_point(points)
            for region, points in face_points.items()
        }

    def _calculate_distances(self, avg_points: dict) -> dict:
        return {
            'forehead_to_nose_distance': self.calculator.calculate_distance(avg_points['forehead'], avg_points['nose']),
            'nose_to_mouth_distance': self.calculator.calculate_distance(avg_points['nose'], avg_points['mouth']),
            'forehead_to_mouth_distance': self.calculator.calculate_distance(avg_points['forehead'], avg_points['mouth']),
        }

    def process(self, face_points: dict) -> dict:
        avg_points = self._average_face_points(face_points)
        distances = self._calculate_distances(avg_points)
        process_head_distances(distances)
        return distances


def receive_head_points(forehead: list, nose: list, mouth: list) -> dict:
    face_points = {
        'forehead': forehead,
        'nose': nose,
        'mouth': mouth,
    }
    processor = HeadDistanceProcessor(EuclideanDistanceCalculator())
    return processor.process(face_points)
