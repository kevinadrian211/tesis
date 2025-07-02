# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/data_reporting/nods_report/nods_reporting.py
from ..report_dispatcher import dispatch_nods_detailed_report, dispatch_nods_summary_report  # Importamos los nuevos enrutadores

# Aseguramos que el contador global esté definido
nod_counter = 0

# Lista de listeners registrados para los reportes detallados de cabeceos
nod_detailed_report_listeners = []

# Lista de listeners registrados para los reportes de resumen de cabeceos
nod_summary_report_listeners = []

def register_nod_listener(callback, report_type="detailed"):
    """
    Permite que otros módulos (como EndReportScreen) reciban los reportes de cabeceos.
    """
    if report_type == "detailed":
        nod_detailed_report_listeners.append(callback)
        print("[INFO] Listener de cabeceo (detallado) registrado.")
    elif report_type == "summary":
        nod_summary_report_listeners.append(callback)
        print("[INFO] Listener de cabeceo (resumen) registrado.")
    else:
        print("[ERROR] Tipo de reporte no válido. Usa 'detailed' o 'summary'.")

def report_nod_data(duration=None):
    global nod_counter  # Declaramos la variable como global para modificarla
    nod_counter += 1
    message = "¡Cabeceo detectado!"  # Mensaje detallado de cabeceo

    # Enviar al dispatcher original
    dispatch_nods_detailed_report(message)

    # Notificar a los listeners registrados para los reportes detallados
    for listener in nod_detailed_report_listeners:
        listener(message)

def report_total_nods():
    """
    Envía un resumen final con la cantidad total de cabeceos detectados.
    """
    summary_message = f"\nTotal de cabeceos detectados: {nod_counter}"
    dispatch_nods_summary_report(summary_message)

    # Notificar a los listeners registrados para los reportes de resumen
    for listener in nod_summary_report_listeners:
        listener(summary_message)

def force_show_report_summary():
    """
    Función pública para forzar el envío del resumen final de cabeceos.
    """
    report_total_nods()
