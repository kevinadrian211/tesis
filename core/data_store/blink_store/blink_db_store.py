# /tesis/core/data_store/blink_store/blink_db_store.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from database import save_blink_minute_report_db as db_save_minute, save_blink_final_report_db as db_save_final

def save_blink_minute_report_db(data: dict):
    """
    Guarda un reporte de parpadeos por minuto en la base de datos
    """
    print(f"[BlinkDBStore] Guardando reporte minuto: {data}")
    return db_save_minute(data)

def save_blink_final_report_db(data: dict):
    """
    Guarda el reporte final de parpadeos en la base de datos
    """
    print(f"[BlinkFinalDBStore] Guardando reporte final: {data}")
    return db_save_final(data)