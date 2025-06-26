# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/pose_extraction/hand_landmarks/hand_landmark_detector.py

import mediapipe as mp
import numpy as np
import cv2
from typing import Tuple, Any, List, Dict
from ..point_router import send_hand_points_to_router


class HandMeshInference:
    def __init__(self, min_detection_confidence=0.6, min_tracking_confidence=0.6):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def process(self, image: np.ndarray) -> Tuple[bool, Any]:
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        hands_landmarks = self.hands.process(rgb_image)
        return bool(hands_landmarks.multi_hand_landmarks), hands_landmarks


class HandMeshExtractor:
    def __init__(self):
        self.points: dict = {}

    def extract_points(self, hand_image: np.ndarray, hand_mesh_info: Any) -> List[List[List[int]]]:
        h, w, _ = hand_image.shape
        mesh_points_per_hand = []
        for hand in hand_mesh_info.multi_hand_landmarks:
            mesh_points = [
                [i, int(pt.x * w), int(pt.y * h)]
                for i, pt in enumerate(hand.landmark)
            ]
            mesh_points_per_hand.append(mesh_points)
        return mesh_points_per_hand

    def extract_feature_points(self, hand_points: List[List[int]], feature_indices: dict):
        self.points = {'hand': {'distances': []}}
        for feature, indices in feature_indices.items():
            for sub_feature, sub_indices in indices.items():
                self.points[feature][sub_feature] = [hand_points[i][1:] for i in sub_indices]

    def get_hand_points(self, all_hand_points: List[List[List[int]]]) -> Dict[str, List[List[List[int]]]]:
        hand_data = []
        indices = list(range(21))  # 21 puntos por mano
        for hand_points in all_hand_points:
            feature_indices = {
                'hand': {
                    'distances': indices
                }
            }
            self.extract_feature_points(hand_points, feature_indices)
            hand_data.append(self.points['hand']['distances'])
        return {'hands': hand_data}


class HandMeshDrawer:
    def __init__(self, color: Tuple[int, int, int] = (255, 0, 0)):
        self.mp_draw = mp.solutions.drawing_utils
        self.config_draw = self.mp_draw.DrawingSpec(color=color, thickness=2, circle_radius=4)  # Aumenté el tamaño de los círculos

    def draw(self, hand_image: np.ndarray, hand_mesh_info: Any):
        for hand_landmarks in hand_mesh_info.multi_hand_landmarks:
            self.mp_draw.draw_landmarks(hand_image, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS,
                                        self.config_draw, self.config_draw)

    def draw_sketch(self, hand_image: np.ndarray, hand_mesh_info: Any) -> np.ndarray:
        h, w, _ = hand_image.shape
        black_image = np.zeros((h, w, 3), dtype=np.uint8)
        for hand_landmarks in hand_mesh_info.multi_hand_landmarks:
            for pt in hand_landmarks.landmark:
                x = int(pt.x * w)
                y = int(pt.y * h)
                z = int(pt.z * 50)  # Cambié este valor para hacerlo más visible
                cv2.circle(black_image, (x, y), 4, (255, 0, 0), -1)  # Aumenté el radio del círculo
        return black_image


class HandMeshProcessor:
    def __init__(self):
        self.inference = HandMeshInference()
        self.extractor = HandMeshExtractor()
        self.drawer = HandMeshDrawer()

    def process(self, hand_image: np.ndarray, draw: bool = True) -> Tuple[dict, bool, np.ndarray]:
        h, w, _ = hand_image.shape
        sketch = np.zeros((h, w, 3), dtype=np.uint8)
        success, hand_mesh_info = self.inference.process(hand_image)
        if not success:
            return {}, success, sketch

        all_hand_points = self.extractor.extract_points(hand_image, hand_mesh_info)
        points = self.extractor.get_hand_points(all_hand_points)

        send_hand_points_to_router(points)

        if draw:
            self.drawer.draw(hand_image, hand_mesh_info)
            sketch = self.drawer.draw_sketch(hand_image, hand_mesh_info)

        return points, success, sketch
