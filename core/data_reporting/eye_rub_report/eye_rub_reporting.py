# core/data_reporting/eye_rub_report/eye_rub_reporting.py

from ..report_dispatcher import print_eye_rub_event, print_eye_rub_final_report

# Contador global de frotamientos de ojos
eye_rub_counter = 0

# IDs temporales para simular estructura de base de datos
DRIVER_ID = 1
TRIP_ID = 1

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
    data_to_db = {
        "driver_id": DRIVER_ID,
        "trip_id": TRIP_ID,
        "gesture_type": "rubbing_eyes",
        "gesture_count": eye_rub_counter
    }
    print_eye_rub_final_report(f"{data_to_db}")

def force_show_report_summary():
    """
    Expone públicamente la función de resumen final.
    """
    report_total_eye_rubs()
