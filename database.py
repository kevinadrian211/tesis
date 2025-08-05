# /tesis/database.py
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import uuid
from typing import Dict, Any
from datetime import datetime

# Cargar las variables de entorno
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL is None or SUPABASE_KEY is None:
    raise ValueError("Las credenciales de Supabase no se han cargado correctamente. Verifica el archivo .env.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------------------------------
# Funciones de utilidad
# ----------------------------------------

def email_exists_in_table(table_name: str, email: str) -> bool:
    try:
        response = supabase.table(table_name).select('id').eq('email', email).limit(1).execute()
        return response.data is not None and len(response.data) > 0
    except Exception as e:
        print(f"Error al verificar existencia de email en '{table_name}': {e}")
        return False

# ----------------------------------------
# Registro de compañía
# ----------------------------------------

def register_company(name, email, password):
    try:
        if email_exists_in_table("companies", email):
            print(f"Ya existe una compañía registrada con el email: {email}")
            return False

        company_id = str(uuid.uuid4())

        response = supabase.table('companies').insert({
            'id': company_id,
            'name': name,
            'email': email,
            'encrypted_password': password  # Almacenar contraseña en texto plano
        }).execute()

        if response.data:
            print(f"Compañía '{name}' registrada exitosamente.")
            return {
                'id': company_id,
                'name': name,
                'email': email
            }
        else:
            print(f"Error al registrar la compañía: {response.error}")
            return False

    except Exception as e:
        print(f"Error al registrar compañía: {e}")
        return False

# ----------------------------------------
# Registro de conductor
# ----------------------------------------

def register_driver(name, email, password, company_id):
    try:
        if email_exists_in_table("users", email):
            print(f"Ya existe un usuario registrado con el email: {email}")
            return False

        driver_id = str(uuid.uuid4())

        response = supabase.table('users').insert({
            'id': driver_id,
            'name': name,
            'email': email,
            'encrypted_password': password,  # Almacenar contraseña en texto plano
            'role': 'driver',
            'company_id': company_id
        }).execute()

        if response.data:
            print(f"Conductor '{name}' registrado exitosamente.")
            return {
                'id': driver_id,
                'name': name,
                'email': email,
                'company_id': company_id
            }
        else:
            print(f"Error al registrar conductor: {response.error}")
            return False

    except Exception as e:
        print(f"Error al registrar conductor: {e}")
        return False

# ----------------------------------------
# Obtener compañías
# ----------------------------------------

def get_all_companies():
    try:
        response = supabase.table('companies').select('id', 'name').execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error al obtener compañías: {e}")
        return []

# ----------------------------------------
# Login de compañía
# ----------------------------------------

def verify_company_login(email: str, password: str):
    try:
        response = supabase.table('companies').select('*').eq('email', email).limit(1).execute()
        if not response.data:
            print(f"Email de compañía no encontrado: {email}")
            return False

        company = response.data[0]
        stored_password = company.get('encrypted_password')

        if stored_password and stored_password == password:
            return company
        else:
            print("Contraseña incorrecta para compañía.")
            return False
    except Exception as e:
        print(f"Error en login de compañía: {e}")
        return False

# ----------------------------------------
# Login de conductor
# ----------------------------------------

def verify_driver_login(email: str, password: str):
    try:
        response = supabase.table('users').select('*').eq('email', email).eq('role', 'driver').limit(1).execute()
        if not response.data:
            print(f"Email de conductor no encontrado: {email}")
            return False

        driver = response.data[0]
        stored_password = driver.get('encrypted_password')

        if stored_password and stored_password == password:
            return driver
        else:
            print("Contraseña incorrecta para conductor.")
            return False
    except Exception as e:
        print(f"Error en login de conductor: {e}")
        return False

# ----------------------------------------
# Registro de administrador
# ----------------------------------------

def register_admin(name, email, password, company_id):
    try:
        if email_exists_in_table("users", email):
            print(f"Ya existe un usuario registrado con el email: {email}")
            return False

        admin_id = str(uuid.uuid4())

        response = supabase.table('users').insert({
            'id': admin_id,
            'name': name,
            'email': email,
            'encrypted_password': password,  # Almacenar contraseña en texto plano
            'role': 'admin',
            'company_id': company_id
        }).execute()

        if response.data:
            print(f"Administrador '{name}' registrado exitosamente.")
            return {
                'id': admin_id,
                'name': name,
                'email': email,
                'company_id': company_id
            }
        else:
            print(f"Error al registrar administrador: {response.error}")
            return False

    except Exception as e:
        print(f"Error al registrar administrador: {e}")
        return False

# ----------------------------------------
# Login de administrador
# ----------------------------------------

def verify_admin_login(email: str, password: str):
    try:
        response = supabase.table('users').select('*').eq('email', email).eq('role', 'admin').limit(1).execute()
        if not response.data:
            print(f"Email de administrador no encontrado: {email}")
            return False

        admin = response.data[0]
        stored_password = admin.get('encrypted_password')

        if stored_password and stored_password == password:
            return admin
        else:
            print("Contraseña incorrecta para administrador.")
            return False
    except Exception as e:
        print(f"Error en login de administrador: {e}")
        return False

# ----------------------------------------
# Funciones para gestión de viajes
# ----------------------------------------

def create_trip(driver_id: str, company_id: str, start_location: str, end_location: str):
    """
    Crea un nuevo viaje en la base de datos
    """
    try:
        trip_id = str(uuid.uuid4())
        
        response = supabase.table('trips').insert({
            'id': trip_id,
            'driver_id': driver_id,
            'company_id': company_id,
            'start_location': start_location,
            'end_location': end_location
        }).execute()

        if response.data:
            print(f"Viaje creado exitosamente con ID: {trip_id}")
            return {
                'id': trip_id,
                'driver_id': driver_id,
                'company_id': company_id,
                'start_location': start_location,
                'end_location': end_location
            }
        else:
            print(f"Error al crear el viaje: {response.error}")
            return False

    except Exception as e:
        print(f"Error al crear viaje: {e}")
        return False

def get_trip_by_id(trip_id: str):
    """
    Obtiene un viaje específico por su ID
    """
    try:
        response = supabase.table('trips').select('*').eq('id', trip_id).limit(1).execute()
        if response.data:
            return response.data[0]
        else:
            print(f"Viaje con ID {trip_id} no encontrado")
            return None
    except Exception as e:
        print(f"Error al obtener viaje: {e}")
        return None

def get_trips_by_driver(driver_id: str):
    """
    Obtiene todos los viajes de un conductor específico
    """
    try:
        response = supabase.table('trips').select('*').eq('driver_id', driver_id).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error al obtener viajes del conductor: {e}")
        return []

def get_trips_by_company(company_id: str):
    """
    Obtiene todos los viajes de una compañía específica
    """
    try:
        response = supabase.table('trips').select('*').eq('company_id', company_id).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error al obtener viajes de la compañía: {e}")
        return []


def save_blink_minute_report_db(data: dict):
    """
    Guarda un reporte de parpadeos por minuto en la base de datos
    """
    try:
        # Preparar datos para inserción
        record = {
            'id': str(uuid.uuid4()),
            'driver_id': data.get('driver_id'),
            'trip_id': data.get('trip_id'),
            'gesture_type': data.get('gesture_type', 'blink'),
            'timestamp': data.get('timestamp', datetime.now().isoformat()),
            'blink_count': data.get('blink_count', 0),
            'blink_avg_duration': float(data.get('blink_avg_duration', 0)),
            'blink_comment': data.get('blink_comment', ''),
            'report_interval_minutes': data.get('report_interval_minutes', 1),
            'created_at': datetime.now().isoformat()
        }
        
        response = supabase.table('blink_minute_reports').insert(record).execute()
        
        if response.data:
            print(f"[BlinkDBStore] Reporte minuto guardado exitosamente: ID {record['id']}")
            return True
        else:
            print(f"[BlinkDBStore] Error al guardar reporte minuto: {response.error}")
            return False
            
    except Exception as e:
        print(f"[BlinkDBStore] Error al guardar reporte minuto: {e}")
        return False

def save_blink_final_report_db(data: dict):
    """
    Guarda el reporte final de parpadeos en la base de datos
    """
    try:
        # Preparar datos para inserción
        record = {
            'id': str(uuid.uuid4()),
            'driver_id': data.get('driver_id'),
            'trip_id': data.get('trip_id'),
            'gesture_type': data.get('gesture_type', 'blink'),
            'normal_reports': data.get('normal_reports', 0),
            'risk_reports': data.get('risk_reports', 0),
            'microsleeps': data.get('microsleeps', 0),
            'total_count': data.get('total_count', 0),
            'comment': data.get('comment', ''),
            'risk_level': data.get('risk_level', 'low'),
            'created_at': datetime.now().isoformat()
        }
        
        response = supabase.table('blink_final_reports').insert(record).execute()
        
        if response.data:
            print(f"[BlinkFinalDBStore] Reporte final guardado exitosamente: ID {record['id']}")
            return True
        else:
            print(f"[BlinkFinalDBStore] Error al guardar reporte final: {response.error}")
            return False
            
    except Exception as e:
        print(f"[BlinkFinalDBStore] Error al guardar reporte final: {e}")
        return False

# ----------------------------------------
# Funciones para reportes de bostezos
# ----------------------------------------

def save_yawn_5min_report_db(data: dict):
    """
    Guarda un reporte de bostezos de 5 minutos en la base de datos
    """
    try:
        record = {
            'id': str(uuid.uuid4()),
            'driver_id': data.get('driver_id'),
            'trip_id': data.get('trip_id'),
            'yawn_count': data.get('yawn_count', 0),
            'avg_duration': data.get('avg_duration'),
            'comment': data.get('comment', ''),
            'report_interval_minutes': 5,
            'created_at': datetime.now().isoformat()
        }
        
        response = supabase.table('yawn_5min_reports').insert(record).execute()
        
        if response.data:
            print(f"[YawnDBStore] Reporte 5min guardado exitosamente: ID {record['id']}")
            return True
        else:
            print(f"[YawnDBStore] Error al guardar reporte 5min: {response.error}")
            return False
            
    except Exception as e:
        print(f"[YawnDBStore] Error al guardar reporte 5min: {e}")
        return False

def save_yawn_10min_report_db(data: dict):
    """
    Guarda un reporte de bostezos de 10 minutos en la base de datos
    """
    try:
        record = {
            'id': str(uuid.uuid4()),
            'driver_id': data.get('driver_id'),
            'trip_id': data.get('trip_id'),
            'yawn_count': data.get('yawn_count', 0),
            'comment': data.get('comment', ''),
            'report_interval_minutes': 10,
            'created_at': datetime.now().isoformat()
        }
        
        response = supabase.table('yawn_10min_reports').insert(record).execute()
        
        if response.data:
            print(f"[YawnDBStore] Reporte 10min guardado exitosamente: ID {record['id']}")
            return True
        else:
            print(f"[YawnDBStore] Error al guardar reporte 10min: {response.error}")
            return False
            
    except Exception as e:
        print(f"[YawnDBStore] Error al guardar reporte 10min: {e}")
        return False

def save_yawn_final_report_db(data: dict):
    """
    Guarda el reporte final de bostezos en la base de datos
    """
    try:
        record = {
            'id': str(uuid.uuid4()),
            'driver_id': data.get('driver_id'),
            'trip_id': data.get('trip_id'),
            'normal_reports': data.get('normal_reports', 0),
            'risk_reports': data.get('risk_reports', 0),
            'created_at': datetime.now().isoformat()
        }
        
        response = supabase.table('yawn_final_reports').insert(record).execute()
        
        if response.data:
            print(f"[YawnFinalDBStore] Reporte final guardado exitosamente: ID {record['id']}")
            return True
        else:
            print(f"[YawnFinalDBStore] Error al guardar reporte final: {response.error}")
            return False
            
    except Exception as e:
        print(f"[YawnFinalDBStore] Error al guardar reporte final: {e}")
        return False

# ----------------------------------------
# Funciones para reportes de frotamiento de ojos
# ----------------------------------------

def save_eye_rub_final_report_db(data: str):
    """
    Guarda el reporte final de frotamiento de ojos en la base de datos
    """
    try:
        # Convertir string a dict si es necesario
        if isinstance(data, str):
            import ast
            try:
                data_dict = ast.literal_eval(data)
            except:
                print(f"[EyeRubDBStore] Error al parsear datos: {data}")
                return False
        else:
            data_dict = data
        
        record = {
            'id': str(uuid.uuid4()),
            'driver_id': data_dict.get('driver_id'),
            'trip_id': data_dict.get('trip_id'),
            'gesture_type': data_dict.get('gesture_type', 'rubbing_eyes'),
            'gesture_count': data_dict.get('gesture_count', 0),
            'created_at': datetime.now().isoformat()
        }
        
        response = supabase.table('eye_rub_final_reports').insert(record).execute()
        
        if response.data:
            print(f"[EyeRubDBStore] Reporte final guardado exitosamente: ID {record['id']}")
            return True
        else:
            print(f"[EyeRubDBStore] Error al guardar reporte final: {response.error}")
            return False
            
    except Exception as e:
        print(f"[EyeRubDBStore] Error al guardar reporte final: {e}")
        return False

# ----------------------------------------
# Funciones para reportes de cabeceo
# ----------------------------------------

def save_nod_final_report_db(data: str):
    """
    Guarda el reporte final de cabeceo en la base de datos
    """
    try:
        # Convertir string a dict si es necesario
        if isinstance(data, str):
            import ast
            try:
                data_dict = ast.literal_eval(data)
            except:
                print(f"[NodDBStore] Error al parsear datos: {data}")
                return False
        else:
            data_dict = data
        
        record = {
            'id': str(uuid.uuid4()),
            'driver_id': data_dict.get('driver_id'),
            'trip_id': data_dict.get('trip_id'),
            'gesture_type': data_dict.get('gesture_type', 'nod'),
            'gesture_count': data_dict.get('gesture_count', 0),
            'created_at': datetime.now().isoformat()
        }
        
        response = supabase.table('nod_final_reports').insert(record).execute()
        
        if response.data:
            print(f"[NodDBStore] Reporte final guardado exitosamente: ID {record['id']}")
            return True
        else:
            print(f"[NodDBStore] Error al guardar reporte final: {response.error}")
            return False
            
    except Exception as e:
        print(f"[NodDBStore] Error al guardar reporte final: {e}")
        return False

# ----------------------------------------
# Funciones de consulta para reportes
# ----------------------------------------

def get_trip_reports(trip_id: str) -> Dict[str, Any]:
    """
    Obtiene todos los reportes asociados a un viaje específico
    """
    try:
        reports = {
            'blink_minute_reports': [],
            'blink_final_reports': [],
            'yawn_5min_reports': [],
            'yawn_10min_reports': [],
            'yawn_final_reports': [],
            'eye_rub_final_reports': [],
            'nod_final_reports': []
        }
        
        # Obtener reportes de parpadeos por minuto
        response = supabase.table('blink_minute_reports').select('*').eq('trip_id', trip_id).execute()
        if response.data:
            reports['blink_minute_reports'] = response.data
        
        # Obtener reportes finales de parpadeos
        response = supabase.table('blink_final_reports').select('*').eq('trip_id', trip_id).execute()
        if response.data:
            reports['blink_final_reports'] = response.data
        
        # Obtener reportes de bostezos 5min
        response = supabase.table('yawn_5min_reports').select('*').eq('trip_id', trip_id).execute()
        if response.data:
            reports['yawn_5min_reports'] = response.data
        
        # Obtener reportes de bostezos 10min
        response = supabase.table('yawn_10min_reports').select('*').eq('trip_id', trip_id).execute()
        if response.data:
            reports['yawn_10min_reports'] = response.data
        
        # Obtener reportes finales de bostezos
        response = supabase.table('yawn_final_reports').select('*').eq('trip_id', trip_id).execute()
        if response.data:
            reports['yawn_final_reports'] = response.data
        
        # Obtener reportes de frotamiento de ojos
        response = supabase.table('eye_rub_final_reports').select('*').eq('trip_id', trip_id).execute()
        if response.data:
            reports['eye_rub_final_reports'] = response.data
        
        # Obtener reportes de cabeceo
        response = supabase.table('nod_final_reports').select('*').eq('trip_id', trip_id).execute()
        if response.data:
            reports['nod_final_reports'] = response.data
        
        return reports
        
    except Exception as e:
        print(f"Error al obtener reportes del viaje {trip_id}: {e}")
        return {}

def get_driver_reports(driver_id: str) -> Dict[str, Any]:
    """
    Obtiene todos los reportes asociados a un conductor específico
    """
    try:
        reports = {
            'blink_minute_reports': [],
            'blink_final_reports': [],
            'yawn_5min_reports': [],
            'yawn_10min_reports': [],
            'yawn_final_reports': [],
            'eye_rub_final_reports': [],
            'nod_final_reports': []
        }
        
        # Obtener reportes de parpadeos por minuto
        response = supabase.table('blink_minute_reports').select('*').eq('driver_id', driver_id).execute()
        if response.data:
            reports['blink_minute_reports'] = response.data
        
        # Obtener reportes finales de parpadeos
        response = supabase.table('blink_final_reports').select('*').eq('driver_id', driver_id).execute()
        if response.data:
            reports['blink_final_reports'] = response.data
        
        # Obtener reportes de bostezos 5min
        response = supabase.table('yawn_5min_reports').select('*').eq('driver_id', driver_id).execute()
        if response.data:
            reports['yawn_5min_reports'] = response.data
        
        # Obtener reportes de bostezos 10min
        response = supabase.table('yawn_10min_reports').select('*').eq('driver_id', driver_id).execute()
        if response.data:
            reports['yawn_10min_reports'] = response.data
        
        # Obtener reportes finales de bostezos
        response = supabase.table('yawn_final_reports').select('*').eq('driver_id', driver_id).execute()
        if response.data:
            reports['yawn_final_reports'] = response.data
        
        # Obtener reportes de frotamiento de ojos
        response = supabase.table('eye_rub_final_reports').select('*').eq('driver_id', driver_id).execute()
        if response.data:
            reports['eye_rub_final_reports'] = response.data
        
        # Obtener reportes de cabeceo
        response = supabase.table('nod_final_reports').select('*').eq('driver_id', driver_id).execute()
        if response.data:
            reports['nod_final_reports'] = response.data
        
        return reports
        
    except Exception as e:
        print(f"Error al obtener reportes del conductor {driver_id}: {e}")
        return {}

# Agregar estas funciones al final de tu archivo database.py

def get_drivers_by_company(company_id: str):
    """
    Obtiene todos los conductores de una compañía específica
    """
    try:
        print(f"Buscando conductores para company_id: {company_id}")
        
        # Consultar la tabla users filtrando por company_id y role = 'driver'
        response = supabase.table('users').select('*').eq('company_id', company_id).eq('role', 'driver').execute()
        
        print(f"Respuesta de la base de datos: {response}")
        
        if response.data:
            print(f"Conductores encontrados: {len(response.data)}")
            # Imprimir detalles de cada conductor
            for driver in response.data:
                print(f"  - {driver.get('name', 'N/A')} ({driver.get('email', 'N/A')})")
            return response.data
        else:
            print("No se encontraron conductores para esta compañía")
            return []
            
    except Exception as e:
        print(f"Error al obtener conductores de la compañía: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_all_trips_by_company(company_id: str):
    """
    Obtiene todos los viajes de una compañía con información del conductor
    """
    try:
        response = supabase.table('trips').select('''
            *,
            users!trips_driver_id_fkey(name, email)
        ''').eq('company_id', company_id).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error al obtener viajes con conductores: {e}")
        return []

def get_trip_reports_summary(trip_id: str):
    """
    Obtiene un resumen de todos los reportes de un viaje
    """
    try:
        summary = {
            'trip_id': trip_id,
            'blink_reports': 0,
            'yawn_reports': 0,
            'eye_rub_reports': 0,
            'nod_reports': 0,
            'risk_level': 'low',
            'total_alerts': 0
        }
        
        # Contar reportes de parpadeos
        blink_response = supabase.table('blink_final_reports').select('*').eq('trip_id', trip_id).execute()
        if blink_response.data:
            summary['blink_reports'] = len(blink_response.data)
            for report in blink_response.data:
                summary['total_alerts'] += report.get('risk_reports', 0)
                if report.get('risk_level') == 'high':
                    summary['risk_level'] = 'high'
                elif report.get('risk_level') == 'moderate' and summary['risk_level'] != 'high':
                    summary['risk_level'] = 'moderate'
        
        # Contar reportes de bostezos
        yawn_response = supabase.table('yawn_final_reports').select('*').eq('trip_id', trip_id).execute()
        if yawn_response.data:
            summary['yawn_reports'] = len(yawn_response.data)
            for report in yawn_response.data:
                summary['total_alerts'] += report.get('risk_reports', 0)
        
        # Contar reportes de frotamiento de ojos
        eye_rub_response = supabase.table('eye_rub_final_reports').select('*').eq('trip_id', trip_id).execute()
        if eye_rub_response.data:
            summary['eye_rub_reports'] = len(eye_rub_response.data)
        
        # Contar reportes de cabeceo
        nod_response = supabase.table('nod_final_reports').select('*').eq('trip_id', trip_id).execute()
        if nod_response.data:
            summary['nod_reports'] = len(nod_response.data)
        
        return summary
        
    except Exception as e:
        print(f"Error al obtener resumen de reportes: {e}")
        return {}

def get_driver_statistics(driver_id: str):
    """
    Obtiene estadísticas generales de un conductor
    """
    try:
        stats = {
            'total_trips': 0,
            'total_alerts': 0,
            'high_risk_trips': 0,
            'moderate_risk_trips': 0,
            'low_risk_trips': 0
        }
        
        # Obtener todos los viajes del conductor
        trips_response = supabase.table('trips').select('id').eq('driver_id', driver_id).execute()
        if trips_response.data:
            stats['total_trips'] = len(trips_response.data)
            
            # Para cada viaje, obtener el resumen de reportes
            for trip in trips_response.data:
                trip_summary = get_trip_reports_summary(trip['id'])
                stats['total_alerts'] += trip_summary.get('total_alerts', 0)
                
                risk_level = trip_summary.get('risk_level', 'low')
                if risk_level == 'high':
                    stats['high_risk_trips'] += 1
                elif risk_level == 'moderate':
                    stats['moderate_risk_trips'] += 1
                else:
                    stats['low_risk_trips'] += 1
        
        return stats
        
    except Exception as e:
        print(f"Error al obtener estadísticas del conductor: {e}")
        return {}

def get_driver_final_reports(driver_id: str):
    """
    Obtiene todos los reportes finales de un conductor específico
    """
    try:
        print(f"Obteniendo reportes finales para driver_id: {driver_id}")
        
        reports = {
            'blink_reports': [],
            'yawn_reports': [],
            'eye_rub_reports': [],
            'nod_reports': []
        }
        
        # Obtener reportes de parpadeo
        try:
            blink_response = supabase.table('blink_final_reports').select('*').eq('driver_id', driver_id).execute()
            if blink_response.data:
                reports['blink_reports'] = blink_response.data
                print(f"Reportes de parpadeo encontrados: {len(blink_response.data)}")
        except Exception as e:
            print(f"Error al obtener reportes de parpadeo: {e}")
        
        # Obtener reportes de bostezos
        try:
            yawn_response = supabase.table('yawn_final_reports').select('*').eq('driver_id', driver_id).execute()
            if yawn_response.data:
                reports['yawn_reports'] = yawn_response.data
                print(f"Reportes de bostezos encontrados: {len(yawn_response.data)}")
        except Exception as e:
            print(f"Error al obtener reportes de bostezos: {e}")
        
        # Obtener reportes de frotamiento de ojos
        try:
            eye_rub_response = supabase.table('eye_rub_final_reports').select('*').eq('driver_id', driver_id).execute()
            if eye_rub_response.data:
                reports['eye_rub_reports'] = eye_rub_response.data
                print(f"Reportes de frotamiento de ojos encontrados: {len(eye_rub_response.data)}")
        except Exception as e:
            print(f"Error al obtener reportes de frotamiento de ojos: {e}")
        
        # Obtener reportes de cabeceo
        try:
            nod_response = supabase.table('nod_final_reports').select('*').eq('driver_id', driver_id).execute()
            if nod_response.data:
                reports['nod_reports'] = nod_response.data
                print(f"Reportes de cabeceo encontrados: {len(nod_response.data)}")
        except Exception as e:
            print(f"Error al obtener reportes de cabeceo: {e}")
        
        # Mostrar resumen
        total_reports = sum(len(reports[key]) for key in reports.keys())
        print(f"Total de reportes finales encontrados: {total_reports}")
        
        return reports
        
    except Exception as e:
        print(f"Error general al obtener reportes finales: {e}")
        import traceback
        traceback.print_exc()
        return {
            'blink_reports': [],
            'yawn_reports': [],
            'eye_rub_reports': [],
            'nod_reports': []
        }

def get_final_reports_by_trip(trip_id: str):
    """
    Obtiene todos los reportes finales asociados a un viaje específico.
    """
    try:
        reports = {
            'blink_reports': [],
            'yawn_reports': [],
            'eye_rub_reports': [],
            'nod_reports': []
        }
        
        # Obtener reportes finales de parpadeos
        response = supabase.table('blink_final_reports').select('*').eq('trip_id', trip_id).execute()
        if response.data:
            reports['blink_reports'] = response.data
        
        # Obtener reportes finales de bostezos
        response = supabase.table('yawn_final_reports').select('*').eq('trip_id', trip_id).execute()
        if response.data:
            reports['yawn_reports'] = response.data
        
        # Obtener reportes finales de frotamiento de ojos
        response = supabase.table('eye_rub_final_reports').select('*').eq('trip_id', trip_id).execute()
        if response.data:
            reports['eye_rub_reports'] = response.data
        
        # Obtener reportes finales de cabeceo
        response = supabase.table('nod_final_reports').select('*').eq('trip_id', trip_id).execute()
        if response.data:
            reports['nod_reports'] = response.data
        
        return reports
        
    except Exception as e:
        print(f"Error al obtener reportes finales por viaje: {e}")
        return {}

def get_minute_reports_by_trip(trip_id: str):
    """
    Obtiene todos los reportes por minuto de un viaje específico
    """
    try:
        response = supabase.table('blink_minute_reports') \
                      .select('*') \
                      .eq('trip_id', trip_id) \
                      .order('timestamp') \
                      .execute()
        
        return response.data if response.data else []
        
    except Exception as e:
        print(f"Error al obtener reportes por minuto: {e}")
        return []

def get_5min_reports_by_trip(trip_id: str):
    """
    Obtiene todos los reportes de 5 minutos de un viaje específico
    """
    try:
        response = supabase.table('yawn_5min_reports') \
                      .select('*') \
                      .eq('trip_id', trip_id) \
                      .order('timestamp') \
                      .execute()
        
        return response.data if response.data else []
        
    except Exception as e:
        print(f"Error al obtener reportes de 5 minutos: {e}")
        return []

def get_10min_reports_by_trip(trip_id: str):
    """
    Obtiene todos los reportes de 10 minutos de un viaje específico
    """
    try:
        response = supabase.table('yawn_10min_reports') \
                      .select('*') \
                      .eq('trip_id', trip_id) \
                      .order('timestamp') \
                      .execute()
        
        return response.data if response.data else []
        
    except Exception as e:
        print(f"Error al obtener reportes de 10 minutos: {e}")
        return []

def get_eye_rub_reports_by_trip(trip_id: str):
    """
    Obtiene todos los reportes de frotamiento de ojos de un viaje específico
    """
    try:
        response = supabase.table('eye_rub_reports') \
                      .select('*') \
                      .eq('trip_id', trip_id) \
                      .order('timestamp') \
                      .execute()
        
        return response.data if response.data else []
        
    except Exception as e:
        print(f"Error al obtener reportes de frotamiento de ojos: {e}")
        return []

def get_nod_reports_by_trip(trip_id: str):
    """
    Obtiene todos los reportes de cabeceo de un viaje específico
    """
    try:
        response = supabase.table('nod_reports') \
                      .select('*') \
                      .eq('trip_id', trip_id) \
                      .order('timestamp') \
                      .execute()
        
        return response.data if response.data else []
        
    except Exception as e:
        print(f"Error al obtener reportes de cabeceo: {e}")
        return []

def get_all_minute_reports_by_trip(trip_id: str):
    """
    Obtiene todos los tipos de reportes por minuto de un viaje específico
    """
    try:
        reports = {
            'blink_minute_reports': get_minute_reports_by_trip(trip_id),
            'yawn_5min_reports': get_5min_reports_by_trip(trip_id),
            'yawn_10min_reports': get_10min_reports_by_trip(trip_id),
            'eye_rub_reports': get_eye_rub_reports_by_trip(trip_id),
            'nod_reports': get_nod_reports_by_trip(trip_id)
        }
        
        return reports
        
    except Exception as e:
        print(f"Error al obtener todos los reportes por minuto: {e}")
        return {}

# Endpoint adicional para obtener estadísticas resumidas
def get_trip_statistics(trip_id: str):
    """
    Obtiene estadísticas resumidas de un viaje específico
    """
    try:
        # Obtener información básica del viaje
        trip_response = supabase.table('trips') \
                          .select('*') \
                          .eq('id', trip_id) \
                          .execute()
        
        if not trip_response.data:
            return {}
        
        trip_info = trip_response.data[0]
        
        # Obtener todos los reportes
        final_reports = get_final_reports_by_trip(trip_id)
        minute_reports = get_all_minute_reports_by_trip(trip_id)
        
        # Calcular estadísticas
        statistics = {
            'trip_info': trip_info,
            'final_reports_summary': {
                'total_blink_reports': len(final_reports.get('blink_reports', [])),
                'total_yawn_reports': len(final_reports.get('yawn_reports', [])),
                'total_eye_rub_reports': len(final_reports.get('eye_rub_reports', [])),
                'total_nod_reports': len(final_reports.get('nod_reports', []))
            },
            'minute_reports_summary': {
                'blink_minute_count': len(minute_reports.get('blink_minute_reports', [])),
                'yawn_5min_count': len(minute_reports.get('yawn_5min_reports', [])),
                'yawn_10min_count': len(minute_reports.get('yawn_10min_reports', [])),
                'eye_rub_count': len(minute_reports.get('eye_rub_reports', [])),
                'nod_count': len(minute_reports.get('nod_reports', []))
            }
        }
        
        return statistics
        
    except Exception as e:
        print(f"Error al obtener estadísticas del viaje: {e}")
        return {}