# core/pose_extraction/hand_landmarks/hand_landmark_detector.py

import mediapipe as mp
import numpy as np
import cv2
from typing import Tuple, Any, List, Dict
from ..point_router import send_hand_points_to_router


# === Inference con MediaPipe Hands ===
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
        results = self.hands.process(rgb_image)
        return bool(results.multi_hand_landmarks), results


# === Extracción de puntos clave por mano ===
class HandMeshExtractor:
    def extract_points(self, image: np.ndarray, mesh_info: Any) -> List[List[List[int]]]:
        h, w, _ = image.shape
        return [
            [[i, int(pt.x * w), int(pt.y * h)] for i, pt in enumerate(hand_landmarks.landmark)]
            for hand_landmarks in mesh_info.multi_hand_landmarks
        ]

    def get_hand_points(self, all_hand_points: List[List[List[int]]]) -> Dict[str, List[List[List[int]]]]:
        hand_data = []
        indices = list(range(21))  # 21 puntos por mano
        for hand_points in all_hand_points:
            filtered = [hand_points[i][1:] for i in indices]
            hand_data.append(filtered)
        return {'hands': hand_data}


# === Dibujo de manos ===
class HandMeshDrawer:
    def __init__(self, color: Tuple[int, int, int] = (255, 0, 0)):
        self.mp_draw = mp.solutions.drawing_utils
        self.config_draw = self.mp_draw.DrawingSpec(color=color, thickness=2, circle_radius=4)

    def draw(self, image: np.ndarray, mesh_info: Any):
        # Dibuja directamente sobre la imagen recibida, sin copiar
        for hand_landmarks in mesh_info.multi_hand_landmarks:
            self.mp_draw.draw_landmarks(
                image,
                hand_landmarks,
                mp.solutions.hands.HAND_CONNECTIONS,
                self.config_draw,
                self.config_draw
            )

    def draw_sketch(self, image: np.ndarray, mesh_info: Any) -> np.ndarray:
        h, w, _ = image.shape
        sketch = np.zeros((h, w, 3), dtype=np.uint8)
        for hand_landmarks in mesh_info.multi_hand_landmarks:
            for pt in hand_landmarks.landmark:
                x = int(pt.x * w)
                y = int(pt.y * h)
                z = int(pt.z * 50)
                cv2.circle(sketch, (x, y), 4, (255, 0, 0), -1)
        return sketch


# === Procesador principal de manos ===
class HandMeshProcessor:
    def __init__(self):
        self.inference = HandMeshInference()
        self.extractor = HandMeshExtractor()
        self.drawer = HandMeshDrawer()

    def process(self, image: np.ndarray, draw: bool = True) -> Tuple[Dict, bool, np.ndarray]:
        # NO hacemos copia interna, dibujamos directamente sobre el frame recibido
        h, w, _ = image.shape
        sketch = np.zeros((h, w, 3), dtype=np.uint8)

        success, mesh_info = self.inference.process(image)
        if not success:
            return {}, success, sketch

        all_hand_points = self.extractor.extract_points(image, mesh_info)
        points = self.extractor.get_hand_points(all_hand_points)
        send_hand_points_to_router(points)

        if draw:
            self.drawer.draw(image, mesh_info)
            return points, success, image
        else:
            return points, success, sketch
