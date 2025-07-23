# yawn_5min_alert.py
from plyer import notification
from .audio_manager import audio_manager

def handle_yawn_5min_report(data: dict):
    print(f"[Yawn5MinAlert] {data}")
    comment = data.get("comment", "").lower()
    if comment != "normal":
        show_notification("Alerta de Bostezos (5min)", "Posible signo de fatiga detectado.")
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
