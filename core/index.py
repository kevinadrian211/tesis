# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/index.py
from pose_extraction.face_landmarks.face_landmark_detector import FaceMeshProcessor
from pose_extraction.hand_landmarks.hand_landmark_detector import HandMeshProcessor
import cv2

face_mesh_processor = FaceMeshProcessor()
hand_mesh_processor = HandMeshProcessor()

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("No se puede acceder a la cámara.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo obtener el frame.")
        break

    frame = cv2.flip(frame, 1)

    face_points, face_success, frame_with_face_mesh = face_mesh_processor.process(frame, draw=True)
    hand_points, hand_success, frame_with_hand_mesh = hand_mesh_processor.process(frame, draw=True)

    frame_with_both_meshes = frame.copy()
    frame_with_both_meshes = cv2.add(frame_with_both_meshes, frame_with_face_mesh)
    frame_with_both_meshes = cv2.add(frame_with_both_meshes, frame_with_hand_mesh)

    cv2.imshow("Cámara Test (Modo Espejo) con Mallas de Cara y Manos", frame_with_both_meshes)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
