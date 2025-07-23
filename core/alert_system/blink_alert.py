# blink_alert.py
from plyer import notification
from .audio_manager import audio_manager

def handle_blink_minute_report(data: dict):
    print(f"[BlinkAlert] {data}")
    comment = data.get("blink_comment", "").strip()
    if is_risk_comment(comment):
        show_notification("Alerta de Fatiga", comment)
        audio_manager.play_notification_sound()

def is_risk_comment(comment: str) -> bool:
    comment = comment.lower()
    return (
        "fatiga" in comment or
        "cansancio" in comment or
        "riesgo" in comment
    )

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
