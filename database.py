from supabase import create_client, Client
from dotenv import load_dotenv
import os
import uuid
import bcrypt  # Importamos bcrypt para cifrar las contraseñas

# Cargar las variables de entorno
load_dotenv()

# Obtener las credenciales de Supabase desde las variables de entorno
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Verificar que las credenciales no sean None
if SUPABASE_URL is None or SUPABASE_KEY is None:
    raise ValueError("Las credenciales de Supabase no se han cargado correctamente. Verifica el archivo .env.")

# Crear el cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Función para cifrar contraseñas
def hash_password(password: str) -> str:
    """Cifra la contraseña usando bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')  # Devolver como string para almacenarlo en la DB

# Función para registrar una nueva compañía
def register_company(name, email, password):
    """
    Registra una nueva compañía en la base de datos.
    """
    try:
        # Generar un UUID para la nueva compañía
        company_id = str(uuid.uuid4())
        
        # Cifrar la contraseña de la compañía
        hashed_password = hash_password(password)
        
        # Insertar los datos de la compañía
        response = supabase.table('companies').insert({
            'id': company_id,
            'name': name,
            'email': email,
            'password': hashed_password  # Guardamos la contraseña cifrada
        }).execute()
        
        # Imprimir la respuesta completa para inspeccionarla
        print("Respuesta completa de Supabase:")
        print(response)

        # Verificamos si se han devuelto datos en la respuesta
        if response.data:
            print(f"Compañía '{name}' registrada exitosamente.")
            return company_id  # Devuelve el ID de la compañía creada
        else:
            print(f"Error al registrar la compañía: No se encontraron datos en la respuesta.")
            print(f"Detalles del error: {response.error}")  # Imprime el detalle del error si está presente
            return False

    except Exception as e:
        print(f"Ocurrió un error al intentar registrar la compañía: {e}")
        return False

def register_driver(name, email, password, company_id):
    """
    Registra un nuevo conductor en la base de datos y lo asocia con una compañía.
    """
    try:
        # Generar un UUID para el nuevo conductor
        driver_id = str(uuid.uuid4())
        
        # Cifrar la contraseña del conductor
        hashed_password = hash_password(password)
        
        # Insertar los datos del conductor
        response = supabase.table('users').insert({
            'id': driver_id,
            'name': name,
            'email': email,
            'encrypted_password': hashed_password,  # Asegúrate de que la contraseña esté cifrada antes de almacenarla
            'role': 'driver',  # Aseguramos que el rol es 'driver'
            'company_id': company_id  # Asignamos el ID de la compañía
        }).execute()
        
        # Imprimir la respuesta completa para inspeccionarla
        print("Respuesta completa de Supabase:")
        print(response)

        # Verificamos si la respuesta contiene datos
        if response.data:
            print(f"Conductor '{name}' registrado exitosamente.")
            return True  # El conductor fue registrado exitosamente
        else:
            print(f"Error al registrar el conductor: No se encontraron datos en la respuesta.")
            print(f"Detalles del error: {response.error}")  # Imprime el detalle del error si está presente
            return False

    except Exception as e:
        print(f"Ocurrió un error al intentar registrar el conductor: {e}")
        return False

# Función para obtener todas las compañías
def get_all_companies():
    """
    Obtiene todas las compañías registradas en la base de datos.
    """
    try:
        # Realizamos la consulta a la base de datos
        response = supabase.table('companies').select('id', 'name').execute()

        # Si la consulta fue exitosa, la propiedad 'data' contendrá los resultados
        companies = response.data if response.data else []

        # Imprimir las compañías obtenidas para depuración
        print(f"Compañías obtenidas de la base de datos: {companies}")

        return companies  # Retornamos la lista de compañías
    except Exception as e:
        print(f"Error al acceder a la base de datos: {e}")
        return []
