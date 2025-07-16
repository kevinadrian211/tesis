import os
import threading
import time
from plyer import notification
from playsound import playsound

# Variables globales para controlar el hilo del sonido de alarma
alarm_thread = None
alarm_playing = False
alarm_lock = threading.Lock()

def handle_microsleep_event(message: str):
    """
    Maneja el evento de microsueño mostrando notificación y reproduciendo alarma
    """
    print(f"[MicrosleepAlert] {message}")
    show_persistent_notification("ALERTA DE MICROSUEÑO", message)
    start_alarm_sound()

def show_persistent_notification(title: str, message: str):
    """
    Muestra una notificación persistente al usuario
    """
    try:
        notification.notify(
            title=title,
            message=message,
            app_name="Fatiga Driver Monitor",
            timeout=0  # 0 significa que no se cierra automáticamente
        )
        print(f"[NOTIFICACIÓN PERSISTENTE] {title} - {message}")
    except Exception as e:
        print(f"[ERROR] No se pudo mostrar la notificación persistente: {e}")

def _play_alarm_loop(sound_path):
    """
    Reproduce el sonido de alarma en bucle hasta que se detenga
    """
    global alarm_playing
    
    while alarm_playing:
        try:
            if os.path.exists(sound_path):
                playsound(sound_path)
            else:
                print(f"[ERROR] Archivo de sonido no encontrado: {sound_path}")
                break
        except Exception as e:
            print(f"[ERROR] Error reproduciendo alarma: {e}")
            break
        
        # Pequeña pausa para evitar que el bucle sea demasiado agresivo
        time.sleep(0.1)

def start_alarm_sound():
    """
    Inicia la reproducción de la alarma en un hilo separado
    """
    global alarm_thread, alarm_playing
    
    with alarm_lock:
        if alarm_playing:
            print("[ALARMA] La alarma ya está sonando")
            return
        
        sound_path = os.path.join(os.path.dirname(__file__), "sounds", "alarm.mp3")
        
        # Verificar que el archivo existe
        if not os.path.exists(sound_path):
            print(f"[ERROR] No se encontró el archivo de sonido: {sound_path}")
            return
        
        alarm_playing = True
        alarm_thread = threading.Thread(
            target=_play_alarm_loop, 
            args=(sound_path,), 
            daemon=True
        )
        alarm_thread.start()
        print(f"[ALARMA] Reproduciendo alarma en bucle: {sound_path}")

def stop_alarm_sound():
    """
    Detiene la reproducción de la alarma
    """
    global alarm_playing
    
    with alarm_lock:
        if alarm_playing:
            alarm_playing = False
            print("[ALARMA] Alarma detenida por el usuario")
        else:
            print("[ALARMA] No hay alarma reproduciéndose")

def is_alarm_playing():
    """
    Verifica si la alarma está sonando actualmente
    """
    return alarm_playing

def reset_alarm_system():
    """
    Reinicia completamente el sistema de alarmas
    """
    global alarm_thread, alarm_playing
    
    with alarm_lock:
        alarm_playing = False
        if alarm_thread and alarm_thread.is_alive():
            alarm_thread.join(timeout=1.0)
        alarm_thread = None
        print("[ALARMA] Sistema de alarmas reiniciado")

# Funciones adicionales para integración con la interfaz
def toggle_alarm():
    """
    Alterna el estado de la alarma (parar/iniciar)
    """
    if alarm_playing:
        stop_alarm_sound()
    else:
        start_alarm_sound()

def get_alarm_status():
    """
    Retorna el estado actual de la alarma
    """
    return {
        'playing': alarm_playing,
        'thread_alive': alarm_thread.is_alive() if alarm_thread else False
    }