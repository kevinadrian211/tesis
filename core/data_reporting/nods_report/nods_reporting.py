# core/data_reporting/nods_report/nods_reporting.py

# Contador global de cabeceos detectados
nod_counter = 0

# IDs temporales (reemplazar con valores reales en producción)
DRIVER_ID = 1
TRIP_ID = 1

# Importar funciones del dispatcher
from ..report_dispatcher import print_nod_event, print_nod_final_report

def report_nod_data(duration=None):
    """
    Se llama cada vez que se detecta un cabeceo.
    Incrementa contador y notifica a través del dispatcher.
    """
    global nod_counter
    nod_counter += 1

    message = "¡Cabeceo detectado!"
    print_nod_event(message)

def report_total_nods():
    """
    Imprime resumen final de cabeceos detectados formateado para base de datos.
    """
    data_to_db = {
        "driver_id": DRIVER_ID,
        "trip_id": TRIP_ID,
        "gesture_type": "nod",
        "gesture_count": nod_counter
    }
    print_nod_final_report(f"{data_to_db}")

def force_show_report_summary():
    """
    Función pública para forzar el envío del resumen final de cabeceos.
    """
    report_total_nods()
