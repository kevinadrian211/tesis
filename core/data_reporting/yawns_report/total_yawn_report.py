# core/data_reporting/yawn_report/total_yawn_report.py
from ..report_dispatcher import (
    print_yawn_event,
    print_yawn_5min_report_db,
    print_yawn_10min_report_db,
    print_yawn_final_report_db,
)
# Importar utilidades para obtener IDs
from ...utils.id_utils import get_driver_id_or_fallback, get_trip_id_or_fallback

# Contadores globales
normal_reports = 0
risk_reports = 0

def send_yawn_event(message: str):
    print_yawn_event(message)

def send_5min_report(message: str, data: dict = None):
    global normal_reports, risk_reports
    
    if data is not None:
        # Asegurar que los IDs están actualizados
        if data.get("driver_id") in [1, None]:
            data["driver_id"] = get_driver_id_or_fallback()
        if data.get("trip_id") in [1, None]:
            data["trip_id"] = get_trip_id_or_fallback()
            
        print_yawn_5min_report_db(data)
    
    if "No se detectó ningún bostezo" in message or "0 bostezo" in message:
        return
    
    if "Signo de cansancio" in message:
        risk_reports += 1
    else:
        normal_reports += 1

def send_10min_report(message: str, data: dict = None):
    global normal_reports, risk_reports
    
    if data is not None:
        # Asegurar que los IDs están actualizados
        if data.get("driver_id") in [1, None]:
            data["driver_id"] = get_driver_id_or_fallback()
        if data.get("trip_id") in [1, None]:
            data["trip_id"] = get_trip_id_or_fallback()
            
        print_yawn_10min_report_db(data)
    
    if "0 bostezo" in message or "No se detectó" in message:
        return
    
    if "Signo de cansancio" in message:
        risk_reports += 1
    else:
        normal_reports += 1

def show_report_summary():
    # Obtener IDs dinámicos
    driver_id = get_driver_id_or_fallback()
    trip_id = get_trip_id_or_fallback()
    
    summary_message = (
        f"\n--- RESUMEN FINAL DE BOSTEZOS REPORTADOS ---\n"
        f"🔵 Reportes normales: {normal_reports}\n"
        f"🔴 Reportes en riesgo: {risk_reports}\n"
        f"----------------------------------"
    )
    
    print(summary_message)
    
    data_to_db = {
        "driver_id": driver_id,
        "trip_id": trip_id,
        "normal_reports": normal_reports,
        "risk_reports": risk_reports,
    }
    
    print_yawn_final_report_db(data_to_db)

def force_show_report_summary():
    show_report_summary()

def reset_yawn_statistics():
    """
    Reinicia las estadísticas para un nuevo viaje.
    """
    global normal_reports, risk_reports
    normal_reports = 0
    risk_reports = 0
    print("[INFO] Estadísticas de bostezos reiniciadas para nuevo viaje")