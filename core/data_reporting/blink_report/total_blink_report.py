# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/data_reporting/blink_report/total_blink_report.py
import atexit
from datetime import datetime

# Contadores globales
normal_reports = 0
risk_reports = 0
microsleep_count = 0

def print_report(message: str):
    global normal_reports, risk_reports, microsleep_count

    # Mostrar el mensaje con marca de tiempo
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

    # Ignorar reportes sin parpadeos
    if "No se detectaron parpadeos" in message:
        return

    # Clasificar el reporte
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

# Mostrar resumen al finalizar
def show_report_summary():
    print("\n--- RESUMEN FINAL DE PARPADEOS ---")
    print(f"🔵 Reportes normales: {normal_reports}")
    print(f"🔴 Reportes en riesgo: {risk_reports}")
    print(f"🛌 Microsueños detectados: {microsleep_count}")
    print("----------------------------------")

# Registrar función para ejecutar al salir
atexit.register(show_report_summary)
