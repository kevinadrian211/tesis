# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/data_reporting/eye_rub_report/eye_rub_reporting.py
import atexit

eye_rub_counter = 0

def report_eye_rub_data():
    global eye_rub_counter
    eye_rub_counter += 1
    print("Frotamiento de ojos detectado.")

def report_total_eye_rubs():
    print(f"\nTotal de frotamientos de ojos detectados: {eye_rub_counter}")


# Agregamos esta función para forzar mostrar resumen manualmente
def force_show_report_summary():
    report_total_eye_rubs()
