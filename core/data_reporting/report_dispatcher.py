from ..report_receivers.gesture_event_receivers import (
    print_minute_report_db as receiver_print_minute_report_db,
    print_eye_rub_event as receiver_print_eye_rub_event,
    print_nod_event as receiver_print_nod_event,
    print_yawn_5min_report_db as receiver_print_yawn_5min_report_db,
    print_yawn_10min_report_db as receiver_print_yawn_10min_report_db,
    print_microsleep_event as receiver_print_microsleep_event,
    print_yawn_event as receiver_print_yawn_event,
)

# Importar la función helper en lugar de la instancia global
from screens_logic.driver_screens_logic.end_report_logic import get_end_report_screen

from core.alert_system.microsleep_alert import handle_microsleep_event
from core.alert_system.blink_alert import handle_blink_minute_report
from core.alert_system.eye_rub_alert import handle_eye_rub_event
from core.alert_system.nod_alert import handle_nod_event
from core.alert_system.yawn_alert import handle_yawn_event
from core.alert_system.yawn_5min_alert import handle_yawn_5min_report
from core.alert_system.yawn_10min_alert import handle_yawn_10min_report

from core.data_store.blink_store.blink_db_store import (
    save_blink_minute_report_db,
    save_blink_final_report_db,
)
from core.data_store.eye_rub_store.eye_rub_db_store import save_eye_rub_final_report_db
from core.data_store.nod_store.nod_db_store import save_nod_final_report_db
from core.data_store.yawn_store.yawn_db_store import (
    save_yawn_5min_report_db,
    save_yawn_10min_report_db,
    save_yawn_final_report_db,
)

def print_blink_event(message: str):
    print(f"[Parpadeo-dispatcher] {message}")

def print_microsleep_event(message: str):
    receiver_print_microsleep_event(message)
    handle_microsleep_event(message)

def print_eye_rub_event(message: str):
    receiver_print_eye_rub_event(message)
    handle_eye_rub_event(message)

def print_nod_event(message: str):
    receiver_print_nod_event(message)
    handle_nod_event(message)

def print_yawn_event(message: str):
    receiver_print_yawn_event(message)
    handle_yawn_event(message)

# === Reportes intermedios ===
def print_minute_report_db(data: dict):
    receiver_print_minute_report_db(data)
    handle_blink_minute_report(data)
    save_blink_minute_report_db(data)

def print_yawn_5min_report_db(data: dict):
    receiver_print_yawn_5min_report_db(data)
    handle_yawn_5min_report(data)
    save_yawn_5min_report_db(data)

def print_yawn_10min_report_db(data: dict):
    receiver_print_yawn_10min_report_db(data)
    handle_yawn_10min_report(data)
    save_yawn_10min_report_db(data)

# === Reportes finales enviados a EndReportScreen ===
def print_final_report_db(data: dict):
    """Envía reporte final de parpadeos a la pantalla de reporte final"""
    print(f"[INFO] Enviando reporte final de parpadeos: {data}")
    
    # Obtener la instancia actual de la pantalla
    screen = get_end_report_screen()
    if screen:
        screen.show_final_blink_report(data)
        print("[INFO] Reporte de parpadeos enviado a EndReportScreen")
    else:
        print("[WARNING] No se pudo encontrar EndReportScreen para actualizar reporte de parpadeos")
    
    # Guardar en base de datos
    save_blink_final_report_db(data)

def print_eye_rub_final_report(message: str):
    """Envía reporte final de frotamiento de ojos a la pantalla de reporte final"""
    print(f"[INFO] Enviando reporte final de frotamiento de ojos: {message}")
    
    # Obtener la instancia actual de la pantalla
    screen = get_end_report_screen()
    if screen:
        screen.show_final_eye_rub_report(message)
        print("[INFO] Reporte de frotamiento de ojos enviado a EndReportScreen")
    else:
        print("[WARNING] No se pudo encontrar EndReportScreen para actualizar reporte de frotamiento")
    
    # Guardar en base de datos
    save_eye_rub_final_report_db(message)

def print_nod_final_report(message: str):
    """Envía reporte final de cabeceo a la pantalla de reporte final"""
    print(f"[INFO] Enviando reporte final de cabeceo: {message}")
    
    # Obtener la instancia actual de la pantalla
    screen = get_end_report_screen()
    if screen:
        screen.show_final_nod_report(message)
        print("[INFO] Reporte de cabeceo enviado a EndReportScreen")
    else:
        print("[WARNING] No se pudo encontrar EndReportScreen para actualizar reporte de cabeceo")
    
    # Guardar en base de datos
    save_nod_final_report_db(message)

def print_yawn_final_report_db(data: dict):
    """Envía reporte final de bostezos a la pantalla de reporte final"""
    print(f"[INFO] Enviando reporte final de bostezos: {data}")
    
    # Obtener la instancia actual de la pantalla
    screen = get_end_report_screen()
    if screen:
        screen.show_final_yawn_report(data)
        print("[INFO] Reporte de bostezos enviado a EndReportScreen")
    else:
        print("[WARNING] No se pudo encontrar EndReportScreen para actualizar reporte de bostezos")
    
    # Guardar en base de datos
    save_yawn_final_report_db(data)