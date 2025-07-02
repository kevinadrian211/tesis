# /Users/kevin/Desktop/tesis/core/data_reporting/yawns_report/total_yawn_report.py
from datetime import datetime
from ..report_dispatcher import dispatch_yawn_detailed_report, dispatch_yawn_summary_report

# Contadores globales de reportes
normal_reports = 0
risk_reports = 0

# Lista de listeners registrados para los reportes detallados de bostezos
yawn_detailed_report_listeners = []

# Lista de listeners registrados para los reportes de resumen de bostezos
yawn_summary_report_listeners = []

def send_report(message: str):
    global normal_reports, risk_reports

    # Agregar timestamp al mensaje
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Enviar reporte detallado
    dispatch_yawn_detailed_report(f"{timestamp} - {message}")

    # Notificar a todos los listeners registrados para los reportes detallados de bostezos
    for listener in yawn_detailed_report_listeners:
        listener(f"{timestamp} - {message}")

    # Clasificar únicamente reportes válidos (que tengan al menos un gesto)
    if message.startswith("[REPORTE 5 MIN]") or message.startswith("[REPORTE 10 MIN]"):
        if "No se detectó ningún bostezo" in message or "Se detectó 0 bostezo" in message:
            return  # Ignorar este mensaje para el conteo

        if "Signo de cansancio" in message:
            risk_reports += 1
        else:
            normal_reports += 1

def show_report_summary():
    """
    Envía el resumen de los bostezos detectados a todos los listeners registrados.
    """
    summary_message = (
        f"\n--- RESUMEN FINAL DE BOSTEZOS REPORTADOS ---\n"
        f"🔵 Reportes normales: {normal_reports}\n"
        f"🔴 Reportes en riesgo: {risk_reports}\n"
        f"----------------------------------"
    )

    # Enviar al dispatcher (se imprimirá en report_dispatcher.py)
    dispatch_yawn_summary_report(summary_message)

    # Notificar a los listeners registrados para los reportes de resumen
    for listener in yawn_summary_report_listeners:
        listener(summary_message)

def force_show_report_summary():
    """
    Función pública para forzar el envío del resumen de bostezos.
    """
    show_report_summary()

# Función para registrar el listener de bostezo
def register_yawn_listener(callback, report_type="detailed"):
    """
    Permite que otros módulos (como EndReportScreen) reciban los reportes de bostezos.
    """
    if report_type == "detailed":
        yawn_detailed_report_listeners.append(callback)
        print("[INFO] Listener de bostezo (detallado) registrado.")
    elif report_type == "summary":
        yawn_summary_report_listeners.append(callback)
        print("[INFO] Listener de bostezo (resumen) registrado.")
    else:
        print("[ERROR] Tipo de reporte no válido. Usa 'detailed' o 'summary'.")
