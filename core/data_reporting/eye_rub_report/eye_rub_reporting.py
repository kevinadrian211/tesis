# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/data_reporting/eye_rub_report/eye_rub_reporting.py
from ..report_dispatcher import dispatch_eye_rub_detailed_report, dispatch_eye_rub_summary_report

# Contador global de frotamientos de ojos
eye_rub_counter = 0

# Lista de funciones externas que desean recibir notificaciones de reportes detallados
eye_rub_detailed_report_listeners = []

# Lista de funciones externas que desean recibir notificaciones de reportes de resumen
eye_rub_summary_report_listeners = []

def register_eye_rub_listener(listener, report_type="detailed"):
    """
    Registra una función que será llamada cada vez que se detecte un frotamiento de ojos.
    Ideal para imprimir en consola o enviar a otras interfaces.

    :param listener: La función que manejará el reporte.
    :param report_type: El tipo de reporte: "detailed" o "summary".
    """
    if report_type == "detailed":
        eye_rub_detailed_report_listeners.append(listener)
        print("[INFO] Listener de frotamiento de ojos (detallado) registrado.")
    elif report_type == "summary":
        eye_rub_summary_report_listeners.append(listener)
        print("[INFO] Listener de frotamiento de ojos (resumen) registrado.")
    else:
        print("[ERROR] Tipo de reporte no válido. Usa 'detailed' o 'summary'.")

def report_eye_rub_data():
    """
    Función que se llama cada vez que se detecta un frotamiento de ojos.
    Incrementa el contador, envía el reporte al dispatcher y notifica a los listeners detallados.
    """
    global eye_rub_counter
    eye_rub_counter += 1

    message = "Frotamiento de ojos detectado."

    # Enviar al sistema de despacho original
    dispatch_eye_rub_detailed_report(message)

    # Notificar a los listeners de reportes detallados
    for listener in eye_rub_detailed_report_listeners:
        listener(message)

def report_total_eye_rubs():
    """
    Envía un resumen final con la cantidad total de eventos detectados.
    """
    summary_message = f"\nTotal de frotamientos de ojos detectados: {eye_rub_counter}"
    dispatch_eye_rub_summary_report(summary_message)

    # Notificar a los listeners de resumen
    for listener in eye_rub_summary_report_listeners:
        listener(summary_message)

def force_show_report_summary():
    """
    Función pública para forzar el envío del resumen final.
    """
    report_total_eye_rubs()
