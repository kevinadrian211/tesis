import os
from plyer import notification
from playsound import playsound

def handle_eye_rub_event(message: str):
    print(f"[EyeRubAlert] {message}")
    
    # Mostrar notificación
    show_notification("Frotamiento de ojos detectado", message)
    
    # Reproducir sonido de alerta
    play_notification_sound()

def show_notification(title: str, message: str):
    try:
        notification.notify(
            title=title,
            message=message,
            app_name="Fatiga Driver Monitor",
            timeout=5
        )
        print(f"[NOTIFICACIÓN] {title} - {message}")
    except Exception as e:
        print(f"[ERROR] No se pudo mostrar la notificación: {e}")

def play_notification_sound():
    try:
        sound_path = os.path.join(os.path.dirname(__file__), "sounds", "notification.mp3")
        playsound(sound_path)
        print(f"[SONIDO] Reproduciendo: {sound_path}")
    except Exception as e:
        print(f"[ERROR] No se pudo reproducir el sonido: {e}")
