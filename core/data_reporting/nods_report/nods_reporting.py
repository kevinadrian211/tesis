# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/data_reporting/nods_report/nods_reporting.py
from ..report_dispatcher import dispatch_nods_detailed_report, dispatch_nods_summary_report  # Importamos los nuevos enrutadores

nod_counter = 0

def report_nod_data(duration=None):
    global nod_counter
    nod_counter += 1
    # Usamos el enrutador para enviar el reporte detallado
    dispatch_nods_detailed_report("¡Cabeceo detectado!")  # Reporte detallado de cabeceo

def report_total_nods():
    # Crear el mensaje de resumen
    summary_message = f"\nTotal de cabeceos detectados: {nod_counter}"
    # Usamos el enrutador para enviar el resumen
    dispatch_nods_summary_report(summary_message)  # Reporte de resumen de cabeceos

# Función adicional para forzar el resumen manualmente
def force_show_report_summary():
    report_total_nods()
