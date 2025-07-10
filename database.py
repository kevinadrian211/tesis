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
            return company_id
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
            return True
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
            return True
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
