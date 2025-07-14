# core/data_reporting/nods_report/nods_reporting.py
# Importar funciones del dispatcher
from ..report_dispatcher import print_nod_event, print_nod_final_report
# Importar utilidades para obtener IDs
from ...utils.id_utils import get_driver_id_or_fallback, get_trip_id_or_fallback

# Contador global de cabeceos detectados
nod_counter = 0

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
    # Obtener IDs dinámicos
    driver_id = get_driver_id_or_fallback()
    trip_id = get_trip_id_or_fallback()
    
    data_to_db = {
        "driver_id": driver_id,
        "trip_id": trip_id,
        "gesture_type": "nod",
        "gesture_count": nod_counter
    }
    
    print_nod_final_report(f"{data_to_db}")

def force_show_report_summary():
    """
    Función pública para forzar el envío del resumen final de cabeceos.
    """
    report_total_nods()

def reset_nod_statistics():
    """
    Reinicia el contador para un nuevo viaje.
    """
    global nod_counter
    nod_counter = 0
    print("[INFO] Estadísticas de cabeceos reiniciadas para nuevo viaje")

def get_nod_count():
    """
    Retorna el contador actual de cabeceos.
    """
    return nod_counter