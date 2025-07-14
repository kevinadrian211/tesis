import threading
from datetime import datetime, timedelta
from .total_yawn_report import send_yawn_event, send_5min_report, send_10min_report

DRIVER_ID = 1
TRIP_ID = 1

yawn_events = []
stop_event = threading.Event()

def report_yawn_data(duration: float):
    timestamp = datetime.now()
    yawn_events.append((timestamp, duration))

    message = f"Duración: {duration:.2f} segundos"
    send_yawn_event(message)

def five_minute_report_loop():
    while not stop_event.is_set():
        if stop_event.wait(timeout=300):
            break

        now = datetime.now()
        window_start = now - timedelta(minutes=5)  # fijar 5 minutos reales
        recent_yawns = [y for y in yawn_events if y[0] >= window_start]
        count = len(recent_yawns)

        if count == 0:
            msg1 = "No se detectó ningún bostezo en los últimos 5 minutos."
            msg2 = "✅ [INFO] Comportamiento dentro de lo normal. Sin señales de cansancio."
            send_5min_report(msg1, data={
                "driver_id": DRIVER_ID,
                "trip_id": TRIP_ID,
                "yawn_count": 0,
                "avg_duration": None,
                "comment": "normal"
            })
            send_5min_report(msg2)
        else:
            durations = [d for _, d in recent_yawns]
            avg_duration = sum(durations) / len(durations)

            if count == 1:
                msg = f"Se detectó 1 bostezo en los últimos 5 minutos. Duración: {avg_duration:.2f} segundos. (Dentro de lo normal)"
            else:
                msg = f"Se detectaron {count} bostezos en los últimos 5 minutos."

            send_5min_report(msg, data={
                "driver_id": DRIVER_ID,
                "trip_id": TRIP_ID,
                "yawn_count": count,
                "avg_duration": f"{avg_duration:.2f}",
                "comment": "normal"
            })

def ten_minute_report_loop():
    while not stop_event.is_set():
        if stop_event.wait(timeout=600):
            break

        now = datetime.now()
        window_start = now - timedelta(minutes=10)  # fijar 10 minutos reales
        recent_yawns = [y for y in yawn_events if y[0] >= window_start]
        count = len(recent_yawns)

        if count == 0:
            msg1 = "No se detectó ningún bostezo en los últimos 10 minutos."
            msg2 = "✅ [INFO] No se detectan señales de cansancio en este periodo."
            send_10min_report(msg1, data={
                "driver_id": DRIVER_ID,
                "trip_id": TRIP_ID,
                "yawn_count": 0,
                "comment": "normal"
            })
            send_10min_report(msg2)
        else:
            if count >= 2:
                msg = f"Se detectaron {count} bostezos en los últimos 10 minutos. Signo de cansancio."
                comment = "riesgo"
            else:
                msg = f"Se detectó {count} bostezo(s) en los últimos 10 minutos. (Dentro de lo normal)"
                comment = "normal"

            send_10min_report(msg, data={
                "driver_id": DRIVER_ID,
                "trip_id": TRIP_ID,
                "yawn_count": count,
                "comment": comment
            })

thread_5min = None
thread_10min = None

def start_reporting():
    global thread_5min, thread_10min
    stop_event.clear()

    thread_5min = threading.Thread(target=five_minute_report_loop, daemon=True)
    thread_10min = threading.Thread(target=ten_minute_report_loop, daemon=True)
    thread_5min.start()
    thread_10min.start()

def stop_reporting():
    stop_event.set()
    if thread_5min is not None:
        thread_5min.join()
    if thread_10min is not None:
        thread_10min.join()
