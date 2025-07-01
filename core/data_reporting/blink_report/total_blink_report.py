# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/data_reporting/blink_report/total_blink_report.py

import atexit
from datetime import datetime
from ..report_dispatcher import dispatch_blink_report  # Importamos el enrutador específico para BlinkReport

# Contadores globales
normal_reports = 0
risk_reports = 0
microsleep_count = 0

def send_report(message: str):
    global normal_reports, risk_reports, microsleep_count

    # Agregar timestamp al mensaje
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dispatch_blink_report(f" {message}")  # Usamos el enrutador para enviar el mensaje

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
    # Mostrar el resumen final de los parpadeos, enviando los mensajes al dispatcher
    dispatch_blink_report("\n--- RESUMEN FINAL DE PARPADEOS ---")
    dispatch_blink_report(f"🔵 Reportes normales: {normal_reports}")
    dispatch_blink_report(f"🔴 Reportes en riesgo: {risk_reports}")
    dispatch_blink_report(f"🛌 Microsueños detectados: {microsleep_count}")
    dispatch_blink_report("----------------------------------")

# Función adicional para forzar el resumen manualmente
def force_show_report_summary():
    show_report_summary()
