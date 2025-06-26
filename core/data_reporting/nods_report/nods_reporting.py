# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/data_reporting/nods_report/nods_reporting.py
import atexit

nod_counter = 0

def report_nod_data(duration=None):
    global nod_counter
    nod_counter += 1
    print(f"¡Cabeceo detectado!")

def report_total_nods():
    print(f"\nTotal de cabeceos detectados: {nod_counter}")

# Agregamos esta función para forzar mostrar resumen manualmente
def force_show_report_summary():
    report_total_nods()
