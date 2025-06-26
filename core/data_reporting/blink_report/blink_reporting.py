# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/data_reporting/blink_report/blink_reporting.py

import time
import threading

# Lógica para imprimir o enviar reportes a la interfaz
ui_report_callback = None  # Se debe asignar desde la UI

def print_report(text):
    global ui_report_callback
    print(text)
    if ui_report_callback:
        ui_report_callback(text)

# Variables globales para almacenar los datos de parpadeos
blink_count = 0
total_duration = 0

# Control del hilo de reporte
reporting_active = False
report_thread = None
lock = threading.Lock()

# Parámetros de referencia
NORMAL_FREQUENCY_MIN = 10
NORMAL_FREQUENCY_MAX = 20
NORMAL_DURATION_MIN = 100
NORMAL_DURATION_MAX = 150
CANSANCIO_DURATION_THRESHOLD = 400
RIESGO_DURATION_MIN = 300
RIESGO_DURATION_MAX = 600

def generate_report():
    global blink_count, total_duration
    while reporting_active:
        time.sleep(60)
        with lock:
            if blink_count == 0:
                print_report("En el último minuto: No se detectaron parpadeos.")
            else:
                average_duration = total_duration / blink_count
                print_report("En el último minuto:")
                print_report(f"- Total de parpadeos: {blink_count}")
                print_report(f"- Duración promedio del parpadeo: {average_duration:.2f} ms")

                if blink_count < NORMAL_FREQUENCY_MIN:
                    if average_duration > CANSANCIO_DURATION_THRESHOLD:
                        print_report("Estado de cansancio: Parpadeos muy lentos y prolongados (> 400 ms).")
                    elif RIESGO_DURATION_MIN <= average_duration <= RIESGO_DURATION_MAX:
                        print_report("⚠️ Riesgo de somnolencia: posibles microsueños (300–600 ms).")
                    else:
                        print_report("Parpadeos poco frecuentes y breves: posible fatiga leve.")
                elif NORMAL_FREQUENCY_MIN <= blink_count <= NORMAL_FREQUENCY_MAX:
                    if NORMAL_DURATION_MIN <= average_duration <= NORMAL_DURATION_MAX:
                        print_report("✅ Parpadeo normal: Frecuencia y duración dentro del rango esperado.")
                    elif average_duration > NORMAL_DURATION_MAX:
                        print_report("Fatiga moderada: parpadeos más lentos de lo normal.")
                    else:
                        print_report("Parpadeos rápidos pero dentro de frecuencia normal.")
                else:
                    print_report("Frecuencia de parpadeo alta: fuera del rango típico.")

            # Reiniciar contadores
            blink_count = 0
            total_duration = 0

def report_blink_data(gesture_type: str, eye: str, duration: float):
    global blink_count, total_duration
    with lock:
        blink_count += 1
        total_duration += duration
    print(f"Datos reportados: {gesture_type.capitalize()} en {eye.capitalize()} con duración de {duration:.0f} ms")

def start_blink_reporting():
    global report_thread, reporting_active
    if reporting_active:
        print("[INFO] El hilo de reporte de parpadeos ya está activo.")
        return

    reporting_active = True
    report_thread = threading.Thread(target=generate_report, daemon=True)
    report_thread.start()
    print("[INFO] Hilo de reporte de parpadeos iniciado.")

def stop_blink_reporting():
    global reporting_active
    reporting_active = False
    print("[INFO] Hilo de reporte de parpadeos detenido.")
