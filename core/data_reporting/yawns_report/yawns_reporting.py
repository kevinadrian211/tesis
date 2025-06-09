# /Users/kevin/Desktop/Piensa/driver-monitoring-app-copy/core/data_reporting/yawns_report/yawns_reporting.py
import time

# Variables para el registro de bostezos
yawn_durations = []
yawn_times = []

# Intervalos de tiempo para clasificar los bostezos
NORMAL_TIME_FRAME = 10 * 60  # 10 minutos en segundos
SLEEPY_TIME_FRAME = 5 * 60   # 5 minutos en segundos

# Variables para controlar el tiempo transcurrido
last_checked_time = time.time()
last_somnolence_check_time = time.time()  # Nuevo control para los 5 minutos de somnolencia

def report_yawn_data(duration: float):
    global last_checked_time, last_somnolence_check_time
    current_time = time.time()  # Obtener el tiempo actual

    # Añadir la duración y el tiempo del bostezo
    yawn_durations.append(duration)
    yawn_times.append(current_time)

    # Imprimir los bostezos cada vez que se detectan
    print(f"[{current_time}] Bostezo detectado. Duración: {duration:.2f} segundos.")

    # Limpiar bostezos que ocurrieron fuera del rango de tiempo relevante para el caso normal
    yawn_durations[:] = [d for d, t in zip(yawn_durations, yawn_times) if current_time - t <= NORMAL_TIME_FRAME]
    yawn_times[:] = [t for t in yawn_times if current_time - t <= NORMAL_TIME_FRAME]

    # Verificar riesgo de somnolencia (2 o más bostezos en los últimos 5 minutos)
    if current_time - last_somnolence_check_time >= SLEEPY_TIME_FRAME:
        recent_yawns_5min = sum(1 for t in yawn_times if current_time - t <= SLEEPY_TIME_FRAME)
        
        if recent_yawns_5min >= 2:
            print(f"[{current_time}] ¡Alerta de riesgo de somnolencia! Se han detectado 2 o más bostezos en los últimos 5 minutos.")
        
        # Reiniciar el contador de tiempo para la somnolencia
        last_somnolence_check_time = current_time

    # Reporte cada 10 minutos: cantidad de bostezos y promedio de la duración
    if current_time - last_checked_time >= NORMAL_TIME_FRAME:
        recent_yawns_10min = len([1 for t in yawn_times if current_time - t <= NORMAL_TIME_FRAME])
        if recent_yawns_10min > 0:
            average_duration = sum(yawn_durations[-recent_yawns_10min:]) / recent_yawns_10min
            print(f"[{current_time}] Reporte de los últimos 10 minutos:")
            print(f"- Total de bostezos detectados: {recent_yawns_10min}")
            print(f"- Duración promedio de los bostezos: {average_duration:.2f} segundos.")
        
        # Reiniciar el contador de tiempo para el reporte de 10 minutos
        last_checked_time = current_time
