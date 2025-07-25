# yawn_alert.py
from plyer import notification
from .audio_manager import audio_manager

def handle_yawn_event(message: str):
    print(f"[YawnAlert] {message}")
    show_notification("Alerta de Bostezo", message)
    audio_manager.play_notification_sound()

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