import atexit
from datetime import datetime
from ..report_dispatcher import dispatch_blink_detailed_report, dispatch_blink_summary_report  # Importamos los nuevos enrutadores

# Contadores globales
normal_reports = 0
risk_reports = 0
microsleep_count = 0

def send_report(message: str):
    global normal_reports, risk_reports, microsleep_count

    # Agregar timestamp al mensaje
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dispatch_blink_detailed_report(f"{timestamp} - {message}")  # Usamos el enrutador para enviar el mensaje detallado

    # Lógica para actualizar contadores basados en el contenido del mensaje
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
    # Enviar el mensaje resumen usando el dispatcher de resumen
    dispatch_blink_summary_report(summary_message)  # Llamamos a la nueva función de resumen

# Función adicional para forzar el resumen manualmente
def force_show_report_summary():
    show_report_summary()
