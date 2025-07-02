# /Users/kevin/Desktop/tesis/core/data_reporting/yawns_report/total_yawn_report.py

from datetime import datetime
from ..report_dispatcher import dispatch_yawn_detailed_report, dispatch_yawn_summary_report  # Importamos los nuevos enrutadores

# Contadores globales de reportes
normal_reports = 0
risk_reports = 0

# Variable global para almacenar el listener
yawn_listener = None

def send_report(message: str):
    global normal_reports, risk_reports

    # Agregar timestamp al mensaje
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dispatch_yawn_detailed_report(f"{timestamp} - {message}")  # Reporte detallado de bostezo

    # Llamar al listener registrado para imprimir en consola
    if yawn_listener:
        yawn_listener(f"{timestamp} - {message}")

    # Clasificar únicamente reportes válidos (que tengan al menos un gesto)
    if message.startswith("[REPORTE 5 MIN]") or message.startswith("[REPORTE 10 MIN]"):
        if "No se detectó ningún bostezo" in message or "Se detectó 0 bostezo" in message:
            return  # Ignorar este mensaje para el conteo

        if "Signo de cansancio" in message:
            risk_reports += 1
        else:
            normal_reports += 1

def show_report_summary():
    summary_message = (
        f"\n--- RESUMEN FINAL DE BOSTEZOS REPORTADOS ---\n"
        f"🔵 Reportes normales: {normal_reports}\n"
        f"🔴 Reportes en riesgo: {risk_reports}\n"
        f"----------------------------------"
    )
    dispatch_yawn_summary_report(summary_message)  # Reporte de resumen de bostezos

def force_show_report_summary():
    show_report_summary()

# Función para registrar el listener de bostezo
def register_yawn_listener(callback):
    global yawn_listener
    yawn_listener = callback
    print("[INFO] Listener de bostezo registrado.")
