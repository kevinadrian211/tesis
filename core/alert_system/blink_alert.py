import os
from plyer import notification
from playsound import playsound

def handle_blink_minute_report(data: dict):
    print(f"[BlinkAlert] {data}")
    
    comment = data.get("blink_comment", "").strip()
    
    if is_risk_comment(comment):
        show_notification("Alerta de Fatiga", comment)
        play_notification_sound()

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

def play_notification_sound():
    try:
        sound_path = os.path.join(os.path.dirname(__file__), "sounds", "notification.mp3")
        playsound(sound_path)
        print(f"[SONIDO] Reproduciendo: {sound_path}")
    except Exception as e:
        print(f"[ERROR] No se pudo reproducir el sonido: {e}")