# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/gesture_detection/gestures.py
from ..data_reporting.blink_report.blink_reporting import report_blink_data
from ..data_reporting.eye_rub_report.eye_rub_reporting import report_eye_rub_data
from ..data_reporting.nods_report.nods_reporting import report_nod_data
from ..data_reporting.yawns_report.yawns_reporting import report_yawn_data


def receive_eye_rub_gesture():
    report_eye_rub_data()

def receive_blink_gesture(eye: str, duration: float):
    report_blink_data('parpadeo', eye, duration)

def receive_microsleep_gesture(eye: str, duration: float):
    report_blink_data('microsueño', eye, duration)


def receive_nod_gesture(duration):
    report_nod_data(duration)

def receive_yawn_gesture(duration):
    report_yawn_data(duration)
