# /tesis/core/data_store/yawn_store/yawn_db_store.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from database import (
    save_yawn_5min_report_db as db_save_5min,
    save_yawn_10min_report_db as db_save_10min,
    save_yawn_final_report_db as db_save_final
)

def save_yawn_5min_report_db(data: dict):
    """
    Guarda un reporte de bostezos de 5 minutos en la base de datos
    """
    print(f"[YawnDBStore] Guardando reporte 5min: {data}")
    return db_save_5min(data)

def save_yawn_10min_report_db(data: dict):
    """
    Guarda un reporte de bostezos de 10 minutos en la base de datos
    """
    print(f"[YawnDBStore] Guardando reporte 10min: {data}")
    return db_save_10min(data)

def save_yawn_final_report_db(data: dict):
    """
    Guarda el reporte final de bostezos en la base de datos
    """
    print(f"[YawnFinalDBStore] Guardando reporte final: {data}")
    return db_save_final(data)