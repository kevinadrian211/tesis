# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/data_reporting/yawns_report/yawns_reporting.py
import threading
import time
from datetime import datetime, timedelta
from .total_yawn_report import print_report

yawn_events = []

def report_yawn_data(duration: float):
    timestamp = datetime.now()
    yawn_events.append((timestamp, duration))
    print_report(f"[REPORTE DE BOSTEZO] Duración: {duration:.2f} segundos | Hora: {timestamp.strftime('%H:%M:%S')}")

def five_minute_report_loop():
    while True:
        time.sleep(300)  # Espera 5 minutos
        now = datetime.now()
        window_start = now - timedelta(minutes=5)
        recent_yawns = [y for y in yawn_events if y[0] >= window_start]
        count = len(recent_yawns)

        if count == 0:
            print_report("[REPORTE 5 MIN] No se detectó ningún bostezo en los últimos 5 minutos.")
            print_report("✅ [INFO] Comportamiento dentro de lo normal. Sin señales de cansancio.")
        elif count == 1:
            _, duration = recent_yawns[0]
            print_report(f"[REPORTE 5 MIN] Se detectó 1 bostezo en los últimos 5 minutos. Duración: {duration:.2f} segundos. (Dentro de lo normal)")
        else:
            print_report(f"[REPORTE 5 MIN] Se detectaron {count} bostezos en los últimos 5 minutos.")
            print_report("⚠️ [ALERTA] Posible signo de cansancio detectado en los últimos 5 minutos.")

def ten_minute_report_loop():
    while True:
        time.sleep(600)  # Espera 10 minutos
        now = datetime.now()
        window_start = now - timedelta(minutes=10)
        recent_yawns = [y for y in yawn_events if y[0] >= window_start]
        count = len(recent_yawns)

        if count >= 2:
            print_report(f"[REPORTE 10 MIN] Se detectaron {count} bostezos en los últimos 10 minutos. Signo de cansancio.")
        else:
            print_report(f"[REPORTE 10 MIN] Se detectó {count} bostezo(s) en los últimos 10 minutos. (Dentro de lo normal)")
            print_report("✅ [INFO] No se detectan señales de cansancio en este periodo.")

def start_reporting():
    print_report("[INFO] Iniciando reportes automáticos cada 5 y 10 minutos...")
    t1 = threading.Thread(target=five_minute_report_loop, daemon=True)
    t2 = threading.Thread(target=ten_minute_report_loop, daemon=True)
    t1.start()
    t2.start()

start_reporting()
