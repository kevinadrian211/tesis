# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/data_reporting/nods_report/nods_reporting.py
from ..report_dispatcher import dispatch_nods_detailed_report, dispatch_nods_summary_report  # Importamos los nuevos enrutadores

# Aseguramos que el contador global esté definido
nod_counter = 0

# Lista de listeners externos (como index.py)
nod_report_listeners = []

def register_nod_listener(listener):
    """Permite que otros módulos reciban los mensajes detallados de cabeceos."""
    nod_report_listeners.append(listener)

def report_nod_data(duration=None):
    global nod_counter  # Declaramos la variable como global para modificarla
    nod_counter += 1
    message = "¡Cabeceo detectado!"  # Mensaje detallado de cabeceo

    # Enviar al dispatcher original
    dispatch_nods_detailed_report(message)

    # Notificar a listeners (como index.py)
    for listener in nod_report_listeners:
        listener(message)

    # (Opcional) También escribir en un archivo:
    # with open("nods_secundario.log", "a", encoding="utf-8") as f:
    #     f.write(message + "\n")

def report_total_nods():
    summary_message = f"\nTotal de cabeceos detectados: {nod_counter}"
    dispatch_nods_summary_report(summary_message)

def force_show_report_summary():
    report_total_nods()
