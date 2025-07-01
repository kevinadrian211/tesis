# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/data_reporting/eye_rub_report/eye_rub_reporting.py
from ..report_dispatcher import dispatch_eye_rub_detailed_report, dispatch_eye_rub_summary_report  # Importamos los nuevos enrutadores

eye_rub_counter = 0

def report_eye_rub_data():
    global eye_rub_counter
    eye_rub_counter += 1
    # Usamos el enrutador para enviar el reporte detallado
    dispatch_eye_rub_detailed_report("Frotamiento de ojos detectado.")  

def report_total_eye_rubs():
    # Crear el mensaje de resumen
    summary_message = f"\nTotal de frotamientos de ojos detectados: {eye_rub_counter}"
    # Usamos el enrutador para enviar el resumen
    dispatch_eye_rub_summary_report(summary_message)  

# Función adicional para forzar el resumen manualmente
def force_show_report_summary():
    report_total_eye_rubs()
