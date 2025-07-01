# /Users/kevin/Desktop/tesis/core/data_reporting/yawns_report/total_yawn_report.py
from datetime import datetime
from ..report_dispatcher import dispatch_yawn_detailed_report, dispatch_yawn_summary_report  # Importamos los nuevos enrutadores

# Contadores globales de reportes
normal_reports = 0
risk_reports = 0

def send_report(message: str):
    global normal_reports, risk_reports

    # Agregar timestamp al mensaje
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Usamos el enrutador para enviar el reporte detallado
    dispatch_yawn_detailed_report(f"{timestamp} - {message}")  # Reporte detallado de bostezo

    # Clasificar únicamente reportes válidos (que tengan al menos un gesto)
    if message.startswith("[REPORTE 5 MIN]") or message.startswith("[REPORTE 10 MIN]"):
        # Excluir mensajes que dicen explícitamente que no hubo bostezos
        if "No se detectó ningún bostezo" in message or "Se detectó 0 bostezo" in message:
            return  # Ignorar este mensaje para el conteo

        # Clasificación de reportes válidos
        if "Signo de cansancio" in message:
            risk_reports += 1
        else:
            normal_reports += 1

def show_report_summary():
    # Crear el mensaje de resumen
    summary_message = (
        f"\n--- RESUMEN FINAL DE BOSTEZOS REPORTADOS ---\n"
        f"🔵 Reportes normales: {normal_reports}\n"
        f"🔴 Reportes en riesgo: {risk_reports}\n"
        f"----------------------------------"
    )
    # Usamos el enrutador para enviar el resumen
    dispatch_yawn_summary_report(summary_message)  # Reporte de resumen de bostezos

# Función para forzar mostrar el resumen en cualquier momento
def force_show_report_summary():
    show_report_summary()
