# core/data_reporting/blink_report/blink_reporting.py
import time
import threading
from datetime import datetime
# Importar funciones para reporte detallado y minute report (DB)
from ..blink_report.total_blink_report import (
    send_report,
    send_minute_report
)
from ..report_dispatcher import (
    print_blink_event,
    print_microsleep_event,
)
# Importar utilidades para obtener IDs
from ...utils.id_utils import get_current_driver_id, get_current_trip_id, get_driver_id_or_fallback, get_trip_id_or_fallback

# ----------------------------
# CONFIGURACIÓN Y UMBRALES
# ----------------------------
NORMAL_FREQUENCY_MIN = 10
NORMAL_FREQUENCY_MAX = 20
NORMAL_DURATION_MIN = 100  # ms
NORMAL_DURATION_MAX = 150
CANSANCIO_DURATION_THRESHOLD = 400
RIESGO_DURATION_MIN = 300
RIESGO_DURATION_MAX = 600
REPORT_INTERVAL_SECONDS = 60

# ----------------------------
# VARIABLES DE ESTADO
# ----------------------------
blink_count = 0
total_duration = 0.0
reporting_active = True
report_thread = None
lock = threading.Lock()

# ----------------------------
# FUNCIONES PRINCIPALES
# ----------------------------
def generate_report():
    global blink_count, total_duration
    while reporting_active:
        time.sleep(REPORT_INTERVAL_SECONDS)
        with lock:
            # Obtener IDs dinámicos
            driver_id = get_driver_id_or_fallback()
            trip_id = get_trip_id_or_fallback()
            
            if blink_count == 0:
                # Solo imprimir mensaje legible cuando no hay parpadeos
                report_message = "En el último minuto: No se detectaron parpadeos."
                print_minute_report(report_message)
                send_report(report_message)
            else:
                average_duration = total_duration / blink_count
                evaluation = evaluate_blink_status(blink_count, average_duration)
                
                # Enviar reporte minuto con IDs reales
                send_minute_report(
                    driver_id=driver_id,
                    trip_id=trip_id,
                    count=blink_count,
                    avg_duration=average_duration,
                    comment=evaluation
                )
                
                # Actualizar estadísticas internas sin imprimir mensaje adicional
                send_report(evaluation)
                
            blink_count = 0
            total_duration = 0.0

def evaluate_blink_status(count: int, avg_duration: float) -> str:
    if count < NORMAL_FREQUENCY_MIN:
        if avg_duration > CANSANCIO_DURATION_THRESHOLD:
            return "Cansancio: Parpadeos muy lentos y prolongados (> 400 ms)."
        elif RIESGO_DURATION_MIN <= avg_duration <= RIESGO_DURATION_MAX:
            return "Riesgo de somnolencia: Microsueños posibles (300–600 ms)."
        else:
            return "Parpadeos escasos y breves: posible fatiga leve."
    elif NORMAL_FREQUENCY_MIN <= count <= NORMAL_FREQUENCY_MAX:
        if NORMAL_DURATION_MIN <= avg_duration <= NORMAL_DURATION_MAX:
            return "Parpadeo normal: frecuencia y duración dentro del rango."
        elif avg_duration > NORMAL_DURATION_MAX:
            return "Fatiga moderada: parpadeos más lentos de lo normal."
        else:
            return "Parpadeos rápidos pero frecuencia adecuada."
    else:
        return "Frecuencia alta de parpadeo: fuera del rango típico."

def report_blink_data(gesture_type: str, eye: str, duration: float):
    global blink_count, total_duration
    with lock:
        blink_count += 1
        total_duration += duration
        
        msg = f"{gesture_type.capitalize()} {eye.capitalize()} {duration:.0f} ms"
        if gesture_type == "parpadeo":
            print_blink_event(msg)
        elif gesture_type == "microsueño":
            print_microsleep_event(msg)

# ----------------------------
# CONTROL DEL HILO DE REPORTE
# ----------------------------
def start_blink_reporting():
    global report_thread, reporting_active
    if report_thread and report_thread.is_alive():
        return
    
    # Validar que tengamos los IDs necesarios
    driver_id = get_current_driver_id()
    trip_id = get_current_trip_id()
    
    if not driver_id or not trip_id:
        print("[WARNING] Iniciando reporte de parpadeos sin IDs válidos")
        print(f"[INFO] driver_id: {driver_id}, trip_id: {trip_id}")
    
    reporting_active = True
    report_thread = threading.Thread(target=generate_report, daemon=True)
    report_thread.start()

def stop_blink_reporting():
    global reporting_active
    reporting_active = False
