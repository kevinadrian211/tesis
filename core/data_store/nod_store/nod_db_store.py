# /tesis/core/data_store/nod_store/nod_db_store.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from database import save_nod_final_report_db as db_save_final

def save_nod_final_report_db(data: str):
    """
    Guarda el reporte final de cabeceo en la base de datos
    """
    print(f"[NodDBStore] Guardando reporte final: {data}")
    return db_save_final(data)