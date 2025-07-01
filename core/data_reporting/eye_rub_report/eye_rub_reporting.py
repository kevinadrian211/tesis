# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/data_reporting/eye_rub_report/eye_rub_reporting.py

from ..report_dispatcher import dispatch_eye_rub_report  # Importamos el enrutador específico para EyeRubReport

eye_rub_counter = 0

def report_eye_rub_data():
    global eye_rub_counter
    eye_rub_counter += 1
    dispatch_eye_rub_report("Frotamiento de ojos detectado.")  # Usamos el dispatcher en lugar de print

def report_total_eye_rubs():
    dispatch_eye_rub_report(f"\nTotal de frotamientos de ojos detectados: {eye_rub_counter}")  # Usamos el dispatcher

# Agregamos esta función para forzar mostrar resumen manualmente
def force_show_report_summary():
    report_total_eye_rubs()
