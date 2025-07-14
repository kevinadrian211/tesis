# core/data_reporting/blink_report/total_blink_report.py
from datetime import datetime
from ..report_dispatcher import print_final_report_db
from ..report_dispatcher import print_minute_report_db
# Importar utilidades para obtener IDs
from ...utils.id_utils import get_driver_id_or_fallback, get_trip_id_or_fallback

# Estadísticas globales
normal_reports = 0
risk_reports = 0
microsleep_count = 0

def send_report(message: str):
    global normal_reports, risk_reports, microsleep_count
    
    if not message.strip():
        # No imprimir ni contar si el mensaje está vacío
        return
    
    print(message)
    
    if "No se detectaron parpadeos" in message:
        return
    
    if "Riesgo de somnolencia" in message:
        risk_reports += 1
        microsleep_count += 1
    elif any(keyword in message for keyword in [
        "Cansancio",
        "Fatiga moderada", 
        "Frecuencia alta de parpadeo",
        "posible fatiga leve"
    ]):
        risk_reports += 1
    elif any(keyword in message for keyword in [
        "Parpadeo normal",
        "Parpadeos rápidos"
    ]):
        normal_reports += 1

def send_minute_report(driver_id, trip_id, count, avg_duration, comment):
    data = {
        "driver_id": driver_id,
        "trip_id": trip_id,
        "gesture_type": "blink",
        "timestamp": datetime.now().isoformat(),
        "blink_count": count,
        "blink_avg_duration": f"{avg_duration:.2f}",
        "blink_comment": comment,
        "report_interval_minutes": 1
    }
    print_minute_report_db(data)

def send_final_report(driver_id=None, trip_id=None):
    # Obtener IDs dinámicos si no se proporcionan
    if driver_id is None:
        driver_id = get_driver_id_or_fallback()
    if trip_id is None:
        trip_id = get_trip_id_or_fallback()
    
    total = normal_reports + risk_reports
    risk_level = "low"
    
    if microsleep_count >= 3 or risk_reports >= 4:
        risk_level = "high"
    elif risk_reports >= 2:
        risk_level = "moderate"
    
    data = {
        "driver_id": driver_id,
        "trip_id": trip_id,
        "gesture_type": "blink",
        "normal_reports": normal_reports,
        "risk_reports": risk_reports,
        "microsleeps": microsleep_count,
        "total_count": total,
        "comment": "Resumen final de parpadeos",
        "risk_level": risk_level
    }
    
    print_final_report_db(data)

def show_report_summary():
    # Obtener IDs dinámicos
    driver_id = get_driver_id_or_fallback()
    trip_id = get_trip_id_or_fallback()
    
    summary_message = (
        "\n--- RESUMEN FINAL DE PARPADEOS ---\n"
        f"🔵 Reportes normales: {normal_reports}\n"
        f"🔴 Reportes en riesgo: {risk_reports}\n"
        f"🛌 Microsueños detectados: {microsleep_count}\n"
        f"----------------------------------\n"
    )
    
    print(summary_message)
    send_final_report(driver_id, trip_id)

def force_show_report_summary():
    show_report_summary()

# Función para reiniciar estadísticas al iniciar un nuevo viaje
def reset_blink_statistics():
    """Reinicia las estadísticas para un nuevo viaje"""
    global normal_reports, risk_reports, microsleep_count
    normal_reports = 0
    risk_reports = 0
    microsleep_count = 0
    print("[INFO] Estadísticas de parpadeos reiniciadas para nuevo viaje")