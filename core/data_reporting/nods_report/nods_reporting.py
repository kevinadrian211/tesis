# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/data_reporting/nods_report/nods_reporting.py

from ..report_dispatcher import dispatch_nods_report  # Importamos el enrutador específico para NodReport

nod_counter = 0

def report_nod_data(duration=None):
    global nod_counter
    nod_counter += 1
    dispatch_nods_report("¡Cabeceo detectado!")  # Usamos el dispatcher en lugar de print

def report_total_nods():
    dispatch_nods_report(f"\nTotal de cabeceos detectados: {nod_counter}")  # Usamos el dispatcher

# Agregamos esta función para forzar mostrar resumen manualmente
def force_show_report_summary():
    report_total_nods()
