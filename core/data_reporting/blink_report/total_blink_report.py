from datetime import datetime
from ..report_dispatcher import print_final_report_db
from ..report_dispatcher import print_minute_report_db

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

def send_final_report(driver_id, trip_id):
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
    summary_message = (
        "\n--- RESUMEN FINAL DE PARPADEOS ---\n"
        f"🔵 Reportes normales: {normal_reports}\n"
        f"🔴 Reportes en riesgo: {risk_reports}\n"
        f"🛌 Microsueños detectados: {microsleep_count}\n"
        f"----------------------------------\n"
    )
    send_final_report(driver_id=1, trip_id=1)

def force_show_report_summary():
    show_report_summary()
