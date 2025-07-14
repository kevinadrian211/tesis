from ..report_dispatcher import (
    print_yawn_event,
    print_yawn_5min_report_db,
    print_yawn_10min_report_db,
    print_yawn_final_report_db,
)

normal_reports = 0
risk_reports = 0

DRIVER_ID = 1
TRIP_ID = 1

def send_yawn_event(message: str):
    print_yawn_event(message)

def send_5min_report(message: str, data: dict = None):
    global normal_reports, risk_reports

    if data is not None:
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
        print_yawn_10min_report_db(data)

    if "0 bostezo" in message or "No se detectó" in message:
        return

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

    data_to_db = {
        "driver_id": DRIVER_ID,
        "trip_id": TRIP_ID,
        "normal_reports": normal_reports,
        "risk_reports": risk_reports,
    }
    print_yawn_final_report_db(data_to_db)

def force_show_report_summary():
    show_report_summary()
