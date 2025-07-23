#microsleep
from plyer import notification
import time
import threading
from .audio_manager import audio_manager

# Variables globales para control de estado
_alarm_start_time = None
_minimum_alarm_duration = 5  # segundos mínimos que debe sonar la alarma
_attention_check_enabled = True

def handle_microsleep_event(message: str):
    """
    Maneja el evento de microsueño mostrando notificación y reproduciendo alarma
    """
    global _alarm_start_time
    
    print(f"[MicrosleepAlert] {message}")
    _alarm_start_time = time.time()
    
    show_persistent_notification("⚠️ ALERTA DE MICROSUEÑO ⚠️", 
                               f"{message}\n\nPresiona el botón 'Desactivar Alarma' cuando estés completamente despierto")
    audio_manager.start_alarm_sound()
    
    # Log para debugging
    print(f"[MICROSUEÑO] Alarma iniciada a las {time.strftime('%H:%M:%S')}")

def show_persistent_notification(title: str, message: str):
    """
    Muestra una notificación persistente al usuario
    """
    try:
        notification.notify(
            title=title,
            app_name="Fatiga Driver Monitor",
            message=message,
            timeout=0  # 0 significa que no se cierra automáticamente
        )
        print(f"[NOTIFICACIÓN PERSISTENTE] {title} - {message}")
    except Exception as e:
        print(f"[ERROR] No se pudo mostrar la notificación persistente: {e}")

def can_dismiss_alarm() -> dict:
    """
    Verifica si la alarma puede ser desactivada de forma segura
    Retorna un diccionario con el estado y razón
    """
    global _alarm_start_time
    
    if not audio_manager.is_alarm_playing():
        return {"can_dismiss": False, "reason": "No hay alarma activa"}
    
    if _alarm_start_time is None:
        return {"can_dismiss": True, "reason": "Sin restricción de tiempo"}
    
    elapsed_time = time.time() - _alarm_start_time
    
    if elapsed_time < _minimum_alarm_duration:
        remaining = _minimum_alarm_duration - elapsed_time
        return {
            "can_dismiss": False, 
            "reason": f"Espera {remaining:.1f} segundos más para asegurar que estás despierto"
        }
    
    return {"can_dismiss": True, "reason": "Alarma puede ser desactivada"}

def dismiss_alarm_safely() -> dict:
    """
    Método seguro para desactivar la alarma con verificaciones
    Retorna resultado de la operación
    """
    # Verificar si se puede desactivar
    check_result = can_dismiss_alarm()
    
    if not check_result["can_dismiss"]:
        print(f"[ALARMA] No se puede desactivar: {check_result['reason']}")
        return {
            "success": False,
            "message": check_result["reason"]
        }
    
    # Desactivar alarma
    audio_manager.stop_alarm_sound()
    
    # Log de la desactivación
    global _alarm_start_time
    if _alarm_start_time:
        duration = time.time() - _alarm_start_time
        print(f"[ALARMA] Desactivada después de {duration:.1f} segundos")
        _alarm_start_time = None
    
    return {
        "success": True,
        "message": "Alarma desactivada correctamente"
    }

def dismiss_alarm_with_attention_check() -> dict:
    """
    Desactiva la alarma requiriendo una prueba de atención
    """
    import random
    
    if not _attention_check_enabled:
        return dismiss_alarm_safely()
    
    # Verificar tiempo mínimo
    check_result = can_dismiss_alarm()
    if not check_result["can_dismiss"]:
        return {
            "success": False,
            "message": check_result["reason"],
            "requires_attention": False
        }
    
    # Generar prueba de atención
    a, b = random.randint(1, 9), random.randint(1, 9)
    expected_answer = a + b
    
    return {
        "success": False,
        "message": f"Para desactivar la alarma, resuelve: {a} + {b} = ?",
        "requires_attention": True,
        "attention_data": {
            "question": f"{a} + {b}",
            "expected_answer": expected_answer
        }
    }

def verify_attention_and_dismiss(user_answer: int, expected_answer: int) -> dict:
    """
    Verifica la respuesta de atención y desactiva la alarma si es correcta
    """
    if user_answer == expected_answer:
        result = dismiss_alarm_safely()
        if result["success"]:
            result["message"] = "✓ Respuesta correcta. " + result["message"]
        return result
    else:
        return {
            "success": False,
            "message": "✗ Respuesta incorrecta. La alarma continuará para tu seguridad."
        }

def stop_alarm_sound():
    """
    Detiene la reproducción de la alarma (método directo)
    NOTA: Para uso en emergencias o debugging
    """
    global _alarm_start_time
    audio_manager.stop_alarm_sound()
    _alarm_start_time = None
    print("[ALARMA] Detenida directamente (método de emergencia)")

def emergency_stop():
    """
    Parada de emergencia - desactiva todo inmediatamente
    """
    global _alarm_start_time
    audio_manager.stop_alarm_sound()
    _alarm_start_time = None
    print("[EMERGENCIA] Sistema de alarmas detenido completamente")

def is_alarm_playing():
    """
    Verifica si la alarma está sonando actualmente
    """
    return audio_manager.is_alarm_playing()

def reset_alarm_system():
    """
    Reinicia completamente el sistema de alarmas
    """
    global _alarm_start_time
    audio_manager.reset_alarm_system()
    _alarm_start_time = None
    print("[SISTEMA] Sistema de alarmas reiniciado")

def toggle_alarm():
    """
    Alterna el estado de la alarma (parar/iniciar)
    """
    audio_manager.toggle_alarm()

def get_alarm_status():
    """
    Retorna el estado actual de la alarma con información adicional
    """
    base_status = audio_manager.get_alarm_status()
    
    global _alarm_start_time
    if _alarm_start_time and base_status['playing']:
        elapsed = time.time() - _alarm_start_time
        base_status['elapsed_time'] = elapsed
        base_status['can_dismiss'] = elapsed >= _minimum_alarm_duration
    
    return base_status

def configure_safety_settings(minimum_duration: int = 5, attention_check: bool = True):
    """
    Configura los parámetros de seguridad de la alarma
    
    Args:
        minimum_duration: Tiempo mínimo en segundos que debe sonar la alarma
        attention_check: Si requiere prueba de atención para desactivar
    """
    global _minimum_alarm_duration, _attention_check_enabled
    _minimum_alarm_duration = minimum_duration
    _attention_check_enabled = attention_check
    
    print(f"[CONFIG] Duración mínima: {minimum_duration}s, Prueba atención: {attention_check}")

# Funciones de conveniencia para la UI
def get_dismiss_button_state():
    """
    Retorna el estado que debe tener el botón de desactivar en la UI
    """
    check = can_dismiss_alarm()
    return {
        "enabled": check["can_dismiss"],
        "text": "Desactivar Alarma" if check["can_dismiss"] else f"Esperar ({check['reason']})",
        "style": "normal" if check["can_dismiss"] else "disabled"
    }

def format_alarm_duration():
    """
    Retorna una cadena formateada con la duración actual de la alarma
    """
    global _alarm_start_time
    if _alarm_start_time and audio_manager.is_alarm_playing():
        elapsed = time.time() - _alarm_start_time
        return f"Alarma activa: {elapsed:.1f}s"
    return "Sin alarma activa"