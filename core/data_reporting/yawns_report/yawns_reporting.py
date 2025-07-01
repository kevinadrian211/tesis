# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/data_reporting/yawns_report/yawns_reporting.py
import threading
from datetime import datetime, timedelta
from .total_yawn_report import send_report  # Importar send_report desde total_yawn_report

yawn_events = []

# Evento para controlar la detención de los hilos
stop_event = threading.Event()

def report_yawn_data(duration: float):
    timestamp = datetime.now()
    yawn_events.append((timestamp, duration))
    # Reemplazar el print por la función send_report de total_yawn_report
    send_report(f"Duración: {duration:.2f} segundos | Hora: {timestamp.strftime('%H:%M:%S')}")

def five_minute_report_loop():
    while not stop_event.is_set():
        # Espera interrumpible de 5 minutos
        if stop_event.wait(timeout=300):
            break

        now = datetime.now()
        window_start = now - timedelta(minutes=5)
        recent_yawns = [y for y in yawn_events if y[0] >= window_start]
        count = len(recent_yawns)

        if count == 0:
            send_report("[REPORTE 5 MIN] No se detectó ningún bostezo en los últimos 5 minutos.")
            send_report("✅ [INFO] Comportamiento dentro de lo normal. Sin señales de cansancio.")
        elif count == 1:
            _, duration = recent_yawns[0]
            send_report(f"[REPORTE 5 MIN] Se detectó 1 bostezo en los últimos 5 minutos. Duración: {duration:.2f} segundos. (Dentro de lo normal)")
        else:
            send_report(f"[REPORTE 5 MIN] Se detectaron {count} bostezos en los últimos 5 minutos.")
            send_report("⚠️ [ALERTA] Posible signo de cansancio detectado en los últimos 5 minutos.")

def ten_minute_report_loop():
    while not stop_event.is_set():
        # Espera interrumpible de 10 minutos
        if stop_event.wait(timeout=600):
            break

        now = datetime.now()
        window_start = now - timedelta(minutes=10)
        recent_yawns = [y for y in yawn_events if y[0] >= window_start]
        count = len(recent_yawns)

        if count >= 2:
            send_report(f"[REPORTE 10 MIN] Se detectaron {count} bostezos en los últimos 10 minutos. Signo de cansancio.")
        else:
            send_report(f"[REPORTE 10 MIN] Se detectó {count} bostezo(s) en los últimos 10 minutos. (Dentro de lo normal)")
            send_report("✅ [INFO] No se detectan señales de cansancio en este periodo.")

# Variables para los hilos
thread_5min = None
thread_10min = None

def start_reporting():
    global thread_5min, thread_10min
    stop_event.clear()
    # Iniciar los reportes utilizando send_report desde total_yawn_report
    send_report("[INFO] Iniciando reportes automáticos cada 5 y 10 minutos...")
    thread_5min = threading.Thread(target=five_minute_report_loop, daemon=True)
    thread_10min = threading.Thread(target=ten_minute_report_loop, daemon=True)
    thread_5min.start()
    thread_10min.start()

def stop_reporting():
    stop_event.set()
    # Opcional: esperar que terminen los hilos
    if thread_5min is not None:
        thread_5min.join()
    if thread_10min is not None:
        thread_10min.join()
