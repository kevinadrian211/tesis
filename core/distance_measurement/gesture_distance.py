# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/distance_measurement/gesture_distance.py
from gesture_detection.blinks.blink_detector import receive_eye_distances as receive_blink_eye_distances
from gesture_detection.eye_rubs.eye_rub_detector import receive_eye_distances as receive_eye_rub_eye_distances
from gesture_detection.eye_rubs.eye_rub_detector import receive_hand_distances as receive_eye_rub_hand_distances
from gesture_detection.nods.nod_detector import receive_head_distances as receive_nod_head_distances
from gesture_detection.yawns.yawn_detector import receive_mouth_distances as receive_yawn_mouth_distances

def process_eye_distances(distances_dict):
    # Enviar las distancias de los ojos a blink_detector.py
    receive_blink_eye_distances(distances_dict)
    
    # Enviar las distancias de los ojos a eye_rub_detector.py
    receive_eye_rub_eye_distances(distances_dict)

def process_hand_distances(distances_dict):
    # Enviar las distancias de las manos a eye_rub_detector.py
    receive_eye_rub_hand_distances(distances_dict)

def process_head_distances(distances_dict):
    # Enviar las distancias de la cabeza a nod_detector.py
    receive_nod_head_distances(distances_dict)

def process_mouth_distances(distances_dict):
    # Enviar las distancias de la boca a yawn_detector.py
    receive_yawn_mouth_distances(distances_dict)




































# from gesture_detection.blinks.blink_detector import receive_eye_distances_from_processor
# from gesture_detection.eye_rubs.eye_rub_detector import receive_hand_to_eye_distances_for_eye_rub_detection
# from gesture_detection.microsleeps.microsleep_detector import (
#     receive_eye_distances_for_microsleep_detection,
#     receive_head_distances_for_microsleep_detection)
# from gesture_detection.nods.nod_detector import receive_head_distances_for_nod_detection
# from gesture_detection.yawns.yawn_detector import receive_mouth_distances_for_yawn_detection

# def process_eye_distances(distances_dict):
#     receive_eye_distances_from_processor(distances_dict)
#     receive_eye_distances_for_microsleep_detection(distances_dict)

# def process_hand_distances(hand_distances_dict):
#     receive_hand_to_eye_distances_for_eye_rub_detection(hand_distances_dict)


# def process_head_distances(head_distances_dict):
#     receive_head_distances_for_nod_detection(head_distances_dict)
#     receive_head_distances_for_microsleep_detection(head_distances_dict)


# def process_mouth_distances(mouth_distances_dict):
#     receive_mouth_distances_for_yawn_detection(mouth_distances_dict)
