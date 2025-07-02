from datetime import datetime
from ..report_dispatcher import dispatch_blink_detailed_report, dispatch_blink_summary_report

# Contadores globales de reportes
normal_reports = 0
risk_reports = 0
microsleep_count = 0

# Lista de listeners registrados para los reportes detallados de parpadeos
blink_detailed_report_listeners = []

# Lista de listeners registrados para los reportes de resumen de parpadeos
blink_summary_report_listeners = []

def send_report(message: str):
    global normal_reports, risk_reports, microsleep_count

    # Agregar timestamp al mensaje
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Enviar reporte detallado
    dispatch_blink_detailed_report(f"{timestamp} - {message}")

    # Notificar a todos los listeners registrados para los reportes detallados de parpadeos
    for listener in blink_detailed_report_listeners:
        listener(f"{timestamp} - {message}")

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
    """
    Envía el resumen de los parpadeos detectados a todos los listeners registrados.
    """
    summary_message = (
        f"--- RESUMEN FINAL DE PARPADEOS ---\n"
        f"🔵 Reportes normales: {normal_reports}\n"
        f"🔴 Reportes en riesgo: {risk_reports}\n"
        f"🛌 Microsueños detectados: {microsleep_count}\n"
        f"----------------------------------"
    )

    # Enviar al dispatcher (se imprimirá en report_dispatcher.py)
    dispatch_blink_summary_report(summary_message)

    # Notificar a los listeners registrados para los reportes de resumen
    for listener in blink_summary_report_listeners:
        listener(summary_message)

def force_show_report_summary():
    """
    Función pública para forzar el envío del resumen de parpadeos.
    """
    show_report_summary()

# Función para registrar el listener de parpadeo
def register_blink_listener(callback, report_type="detailed"):
    """
    Permite que otros módulos (como EndReportScreen) reciban los reportes de parpadeos.
    """
    if report_type == "detailed":
        blink_detailed_report_listeners.append(callback)
        print("[INFO] Listener de parpadeo (detallado) registrado.")
    elif report_type == "summary":
        blink_summary_report_listeners.append(callback)
        print("[INFO] Listener de parpadeo (resumen) registrado.")
    else:
        print("[ERROR] Tipo de reporte no válido. Usa 'detailed' o 'summary'.")
