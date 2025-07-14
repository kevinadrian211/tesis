# core/pose_extraction/face_landmarks/face_landmark_detector.py

import mediapipe as mp
import numpy as np
import cv2
from typing import Tuple, Any, List, Dict
from ..point_router import send_face_points_to_router


# === Inference con MediaPipe ===
class FaceMeshInference:
    def __init__(self, min_detection_confidence=0.6, min_tracking_confidence=0.6):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def process(self, image: np.ndarray) -> Tuple[bool, Any]:
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_image)
        return bool(results.multi_face_landmarks), results


# === Extracción de puntos relevantes del rostro ===
class FaceMeshExtractor:
    def __init__(self):
        self.points = {
            'eyes': {'distances': []},
            'mouth': {'distances': []},
            'head': {'distances': []},
            'nose': {'distances': []},
            'chin': {'distances': []},
        }

    def extract_points(self, image: np.ndarray, face_mesh_info: Any) -> List[List[int]]:
        h, w, _ = image.shape
        return [
            [i, int(pt.x * w), int(pt.y * h)]
            for face in face_mesh_info.multi_face_landmarks
            for i, pt in enumerate(face.landmark)
        ]

    def extract_feature_points(self, face_points: List[List[int]], feature_indices: dict):
        for feature, indices in feature_indices.items():
            for sub_feature, sub_indices in indices.items():
                self.points[feature][sub_feature] = [face_points[i][1:] for i in sub_indices]

    def get_eyes_points(self, face_points: List[List[int]]):
        self.extract_feature_points(face_points, {
            'eyes': {
                'distances': [159, 145, 385, 374, 468, 472, 473, 477, 468, 473],
            }
        })
        return self.points['eyes']

    def get_mouth_points(self, face_points: List[List[int]]):
        self.extract_feature_points(face_points, {
            'mouth': {
                'distances': [13, 14, 17, 199],
            }
        })
        return self.points['mouth']

    def get_head_points(self, face_points: List[List[int]]):
        self.extract_feature_points(face_points, {
            'head': {
                'distances': [1, 0, 1, 5, 4, 205, 425],
            }
        })
        return self.points['head']

    def get_nose_points(self, face_points: List[List[int]]):
        self.extract_feature_points(face_points, {
            'nose': {
                'distances': [1, 2, 3, 4, 5],
            }
        })
        return self.points['nose']

    def get_chin_points(self, face_points: List[List[int]]):
        self.extract_feature_points(face_points, {
            'chin': {
                'distances': [152, 154, 176, 157],
            }
        })
        return self.points['chin']


# === Dibujo de la malla facial ===
class FaceMeshDrawer:
    def __init__(self, color: Tuple[int, int, int] = (255, 255, 0)):
        self.mp_draw = mp.solutions.drawing_utils
        self.config_draw = self.mp_draw.DrawingSpec(color=color, thickness=1, circle_radius=1)

    def draw(self, image: np.ndarray, face_mesh_info: Any):
        # Dibuja directamente sobre la imagen recibida, sin hacer copia
        for face in face_mesh_info.multi_face_landmarks:
            self.mp_draw.draw_landmarks(
                image,
                face,
                mp.solutions.face_mesh.FACEMESH_TESSELATION,
                self.config_draw,
                self.config_draw
            )

    def draw_sketch(self, image: np.ndarray, face_mesh_info: Any) -> np.ndarray:
        h, w, _ = image.shape
        sketch = np.zeros((h, w, 3), dtype=np.uint8)
        for face in face_mesh_info.multi_face_landmarks:
            for pt in face.landmark:
                x = int(pt.x * w)
                y = int(pt.y * h)
                z = int(pt.z * 50)
                cv2.circle(sketch, (x, y), 1, (255 - z, 255 - z, 0 - z), -1)
        return sketch


# === Procesador principal ===
class FaceMeshProcessor:
    def __init__(self):
        self.inference = FaceMeshInference()
        self.extractor = FaceMeshExtractor()
        self.drawer = FaceMeshDrawer()

    def process(self, image: np.ndarray, draw: bool = True) -> Tuple[Dict, bool, np.ndarray]:
        # NO hacemos copia aquí, dibujamos sobre la imagen original que llega
        h, w, _ = image.shape
        sketch = np.zeros((h, w, 3), dtype=np.uint8)

        success, face_mesh_info = self.inference.process(image)
        if not success:
            return {}, success, sketch

        face_points = self.extractor.extract_points(image, face_mesh_info)

        points = {
            'eyes': self.extractor.get_eyes_points(face_points),
            'mouth': self.extractor.get_mouth_points(face_points),
            'forehead': self.extractor.get_head_points(face_points),
            'nose': self.extractor.get_nose_points(face_points),
            'chin': self.extractor.get_chin_points(face_points),
        }

        send_face_points_to_router(points)

        if draw:
            self.drawer.draw(image, face_mesh_info)
            return points, success, image
        else:
            return points, success, sketch
