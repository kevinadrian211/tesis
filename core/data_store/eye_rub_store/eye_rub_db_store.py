# /tesis/core/data_store/eye_rub_store/eye_rub_db_store.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from database import save_eye_rub_final_report_db as db_save_final

def save_eye_rub_final_report_db(data: str):
    """
    Guarda el reporte final de frotamiento de ojos en la base de datos
    """
    print(f"[EyeRubDBStore] Guardando reporte final: {data}")
    return db_save_final(data)