# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/data_reporting/eye_rub_report/eye_rub_reporting.py

from ..report_dispatcher import dispatch_eye_rub_detailed_report, dispatch_eye_rub_summary_report

# Contador global de frotamientos de ojos
eye_rub_counter = 0

# Lista de funciones externas que desean recibir notificaciones de reportes (como index.py)
eye_rub_report_listeners = []

def register_eye_rub_listener(listener):
    """
    Registra una función que será llamada cada vez que se detecte un frotamiento de ojos.
    Ideal para imprimir en consola o enviar a otras interfaces.
    """
    eye_rub_report_listeners.append(listener)

def report_eye_rub_data():
    """
    Función que se llama cada vez que se detecta un frotamiento de ojos.
    Incrementa el contador, envía el reporte al dispatcher y notifica a los listeners.
    """
    global eye_rub_counter
    eye_rub_counter += 1

    message = "Frotamiento de ojos detectado."

    # Enviar al sistema de despacho original
    dispatch_eye_rub_detailed_report(message)

    # Notificar a los listeners registrados (como index.py)
    for listener in eye_rub_report_listeners:
        listener(message)

    # (Opcional) También podrías registrar en un archivo:
    # with open("eye_rub_secondary.log", "a", encoding="utf-8") as f:
    #     f.write(f"{message}\n")

def report_total_eye_rubs():
    """
    Envía un resumen final con la cantidad total de eventos detectados.
    """
    summary_message = f"\nTotal de frotamientos de ojos detectados: {eye_rub_counter}"
    dispatch_eye_rub_summary_report(summary_message)

def force_show_report_summary():
    """
    Función pública para forzar el envío del resumen final.
    """
    report_total_eye_rubs()
