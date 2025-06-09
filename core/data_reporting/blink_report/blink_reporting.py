#  /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/data_reporting/blink_report/blink_reporting.py
import time

# Variables globales para almacenar los datos de parpadeos
blink_count = 0  # Contador de parpadeos
total_duration = 0  # Suma total de las duraciones de los parpadeos
last_report_time = time.time()  # Momento del último informe

# Parámetros de referencia
SOMNOLENCE_FREQUENCY_THRESHOLD = 10  # Frecuencia de parpadeos para somnolencia
SLEEPY_FREQUENCY_THRESHOLD = 20  # Frecuencia de parpadeos para cansancio
SOMNOLENCE_DURATION_THRESHOLD = 400  # Duración de parpadeos en ms para somnolencia
SLEEPY_DURATION_THRESHOLD = 150  # Duración de parpadeos en ms para cansancio
RISKY_DURATION_THRESHOLD_HIGH = 600  # Limite superior de duración de parpadeos para riesgo de somnolencia

# Lógica para recibir parpadeos y calcular el estado
def report_blink_data(gesture_type: str, eye: str, duration: float):
    global blink_count, total_duration, last_report_time

    # Incrementar el contador y la duración total
    blink_count += 1
    total_duration += duration

    # Obtener el tiempo actual
    current_time = time.time()

    # Verificar si ha pasado un minuto desde el último informe
    if current_time - last_report_time >= 60:
        # Calcular el promedio de la duración de los parpadeos
        average_duration = total_duration / blink_count if blink_count > 0 else 0

        # Imprimir la cantidad de parpadeos y la duración promedio
        print(f"En el último minuto:")
        print(f"- Total de parpadeos: {blink_count}")
        print(f"- Duración promedio del parpadeo: {average_duration:.2f} ms")

        # Evaluación del estado de somnolencia con los nuevos umbrales
        if blink_count < SOMNOLENCE_FREQUENCY_THRESHOLD:
            if average_duration > SOMNOLENCE_DURATION_THRESHOLD:
                print("¡Posible estado de somnolencia! El parpadeo es lento y prolongado.")
            elif average_duration >= 300 and average_duration <= RISKY_DURATION_THRESHOLD_HIGH:
                print("Riesgo de somnolencia: Parpadeos lentos detectados, indicando posibles microsueños.")
            else:
                print("Riesgo de somnolencia: Parpadeos muy rápidos y poco frecuentes.")
        elif blink_count >= SOMNOLENCE_FREQUENCY_THRESHOLD and blink_count <= SLEEPY_FREQUENCY_THRESHOLD:
            if average_duration > SLEEPY_DURATION_THRESHOLD:
                print("Cansancio: Parpadeos más lentos y frecuentes de lo normal.")
            else:
                print("Frecuencia dentro del rango normal, pero duración del parpadeo menor al esperado.")
        else:
            print("Frecuencia y duración dentro del rango normal de parpadeo.")

        # Reiniciar los contadores para el siguiente minuto
        blink_count = 0
        total_duration = 0
        last_report_time = current_time

    # Imprimir los datos del parpadeo detectado
    print(f"Datos reportados: {gesture_type.capitalize()} en {eye.capitalize()} con duración de {duration:.0f} ms")
