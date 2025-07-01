# /Users/kevin/Desktop/tesis/core/data_reporting/yawns_report/total_yawn_report.py
import atexit
from datetime import datetime

# Contadores globales de reportes
normal_reports = 0
risk_reports = 0

def print_report(message: str):
    global normal_reports, risk_reports

    # Mostrar siempre el mensaje con timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

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

# Imprimir resumen al finalizar el programa
def show_report_summary():
    print("\n--- RESUMEN FINAL DE BOSTEZOS REPORTADOS ---")
    print(f"🔵 Reportes normales: {normal_reports}")
    print(f"🔴 Reportes en riesgo: {risk_reports}")
    print("----------------------------------")

# Función para forzar mostrar el resumen en cualquier momento
def force_show_report_summary():
    show_report_summary()
