# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/distance_measurement/gesture_distance.py
from ..gesture_detection.blinks.blink_detector import receive_eye_distances as receive_blink_eye_distances
from ..gesture_detection.eye_rubs.eye_rub_detector import receive_eye_distances as receive_eye_rub_eye_distances
from ..gesture_detection.eye_rubs.eye_rub_detector import receive_hand_distances as receive_eye_rub_hand_distances
from ..gesture_detection.nods.nod_detector import receive_head_distances as receive_nod_head_distances
from ..gesture_detection.yawns.yawn_detector import receive_mouth_distances as receive_yawn_mouth_distances


def process_eye_distances(distances_dict):
    receive_blink_eye_distances(distances_dict)
    receive_eye_rub_eye_distances(distances_dict)

def process_hand_distances(distances_dict):
    receive_eye_rub_hand_distances(distances_dict)

def process_head_distances(distances_dict):
    receive_nod_head_distances(distances_dict)

def process_mouth_distances(distances_dict):
    receive_yawn_mouth_distances(distances_dict)
