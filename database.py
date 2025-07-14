from supabase import create_client, Client
from dotenv import load_dotenv
import os
import uuid
import bcrypt

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

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

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
        hashed_password = hash_password(password)

        response = supabase.table('companies').insert({
            'id': company_id,
            'name': name,
            'email': email,
            'encrypted_password': hashed_password
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
        hashed_password = hash_password(password)

        response = supabase.table('users').insert({
            'id': driver_id,
            'name': name,
            'email': email,
            'encrypted_password': hashed_password,
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
        stored_hash = company.get('encrypted_password')

        if stored_hash and bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
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
        stored_hash = driver.get('encrypted_password')

        if stored_hash and bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
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
        hashed_password = hash_password(password)

        response = supabase.table('users').insert({
            'id': admin_id,
            'name': name,
            'email': email,
            'encrypted_password': hashed_password,
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
        stored_hash = admin.get('encrypted_password')

        if stored_hash and bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
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