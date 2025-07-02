import atexit
from datetime import datetime
from ..report_dispatcher import (
    dispatch_blink_detailed_report,
    dispatch_blink_summary_report
)

# Contadores globales
normal_reports = 0
risk_reports = 0
microsleep_count = 0

# Lista de funciones externas (listeners) que quieren recibir los mensajes
report_listeners = []

def register_report_listener(listener):
    """Permite que otros módulos se suscriban a los mensajes detallados."""
    report_listeners.append(listener)

def send_report(message: str):
    global normal_reports, risk_reports, microsleep_count

    # Agregar timestamp al mensaje
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_message = f"{timestamp} - {message}"

    # Enviar al dispatcher original
    dispatch_blink_detailed_report(full_message)

    # Guardar también en un archivo local secundario
    with open("parpadeos_secundario.log", "a", encoding="utf-8") as f:
        f.write(full_message + "\n")

    # Notificar a cualquier listener registrado (por ejemplo, index.py)
    for listener in report_listeners:
        listener(full_message)

    # Clasificación del mensaje para estadísticas
    if "No se detectaron parpadeos" in message:
        return

    if "Riesgo de somnolencia" in message:
        risk_reports += 1
        microsleep_count += 1
    elif any(keyword in message for keyword in [
        "Estado de cansancio",
        "Fatiga moderada",
        "Frecuencia de parpadeo alta",
        "Parpadeos poco frecuentes"
    ]):
        risk_reports += 1
    elif any(keyword in message for keyword in [
        "Parpadeo normal",
        "Parpadeos rápidos"
    ]):
        normal_reports += 1

def show_report_summary():
    # Crear el mensaje resumen
    summary_message = (
        f"--- RESUMEN FINAL DE PARPADEOS ---\n"
        f"🔵 Reportes normales: {normal_reports}\n"
        f"🔴 Reportes en riesgo: {risk_reports}\n"
        f"🛌 Microsueños detectados: {microsleep_count}\n"
        f"----------------------------------"
    )

    # Enviar el resumen usando el dispatcher
    dispatch_blink_summary_report(summary_message)

# Función para forzar el envío del resumen (por ejemplo, al final del monitoreo)
def force_show_report_summary():
    show_report_summary()

# Registrar resumen automático al salir, si lo deseas
# atexit.register(show_report_summary)
