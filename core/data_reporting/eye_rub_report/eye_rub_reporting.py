# core/data_reporting/eye_rub_report/eye_rub_reporting.py
from ..report_dispatcher import print_eye_rub_event, print_eye_rub_final_report
# Importar utilidades para obtener IDs
from ...utils.id_utils import get_driver_id_or_fallback, get_trip_id_or_fallback

# Contador global de frotamientos de ojos
eye_rub_counter = 0

def report_eye_rub_data():
    """
    Se llama cada vez que se detecta un frotamiento de ojos.
    Incrementa el contador y muestra mensaje en consola.
    """
    global eye_rub_counter
    eye_rub_counter += 1
    
    message = "Frotamiento de ojos detectado."
    print_eye_rub_event(message)

def report_total_eye_rubs():
    """
    Imprime un resumen final en formato listo para base de datos.
    """
    # Obtener IDs dinámicos
    driver_id = get_driver_id_or_fallback()
    trip_id = get_trip_id_or_fallback()
    
    data_to_db = {
        "driver_id": driver_id,
        "trip_id": trip_id,
        "gesture_type": "rubbing_eyes",
        "gesture_count": eye_rub_counter
    }
    
    print_eye_rub_final_report(f"{data_to_db}")

def force_show_report_summary():
    """
    Expone públicamente la función de resumen final.
    """
    report_total_eye_rubs()

def reset_eye_rub_statistics():
    """
    Reinicia el contador para un nuevo viaje.
    """
    global eye_rub_counter
    eye_rub_counter = 0
    print("[INFO] Estadísticas de frotamiento de ojos reiniciadas para nuevo viaje")

def get_eye_rub_count():
    """
    Retorna el contador actual de frotamientos de ojos.
    """
    return eye_rub_counter