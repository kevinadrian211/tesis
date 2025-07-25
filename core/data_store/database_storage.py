# /tesis/core/data_store/database_storage.py

"""
Módulo puente para conectar los stores con las funciones de database.py
"""

import sys
import os

# Añadir la ruta raíz del proyecto al path para poder importar database.py
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

# Importar las funciones desde database.py
from database import (
    save_blink_minute_report_db,
    save_blink_final_report_db,
    save_yawn_5min_report_db,
    save_yawn_10min_report_db,
    save_yawn_final_report_db,
    save_eye_rub_final_report_db,
    save_nod_final_report_db
)