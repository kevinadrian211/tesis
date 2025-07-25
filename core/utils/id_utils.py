# core/utils/id_utils.py
"""
Utilidades para obtener los IDs del conductor y viaje actual
desde cualquier parte del sistema de reportes.
"""

from kivy.app import App

def get_current_driver_id():
    """
    Obtiene el ID del conductor actualmente logueado.
    
    Returns:
        str: ID del conductor o None si no hay usuario logueado
    """
    try:
        app = App.get_running_app()
        if app and hasattr(app, 'current_user') and app.current_user:
            user = app.current_user
            if user.get('role') == 'driver':
                return user.get('id')
        return None
    except Exception as e:
        print(f"[ERROR] Error obteniendo driver_id: {e}")
        return None

def get_current_trip_id():
    """
    Obtiene el ID del viaje actual.
    
    Returns:
        str: ID del viaje o None si no hay viaje activo
    """
    try:
        app = App.get_running_app()
        if app and hasattr(app, 'current_trip') and app.current_trip:
            return app.current_trip.get('id')
        return None
    except Exception as e:
        print(f"[ERROR] Error obteniendo trip_id: {e}")
        return None

def get_current_company_id():
    """
    Obtiene el ID de la compañía del conductor actual.
    
    Returns:
        str: ID de la compañía o None si no hay usuario logueado
    """
    try:
        app = App.get_running_app()
        if app and hasattr(app, 'current_user') and app.current_user:
            user = app.current_user
            if user.get('role') == 'driver':
                return user.get('company_id')
        return None
    except Exception as e:
        print(f"[ERROR] Error obteniendo company_id: {e}")
        return None

def get_current_ids():
    """
    Obtiene todos los IDs relevantes de una vez.
    
    Returns:
        dict: Diccionario con driver_id, trip_id y company_id
    """
    return {
        'driver_id': get_current_driver_id(),
        'trip_id': get_current_trip_id(),
        'company_id': get_current_company_id()
    }

def validate_ids():
    """
    Valida que los IDs necesarios estén disponibles.
    
    Returns:
        bool: True si driver_id y trip_id están disponibles
    """
    driver_id = get_current_driver_id()
    trip_id = get_current_trip_id()
    
    if not driver_id:
        print("[WARNING] No hay driver_id disponible")
        return False
    
    if not trip_id:
        print("[WARNING] No hay trip_id disponible")
        return False
    
    return True

# Funciones de respaldo para casos donde los IDs no estén disponibles
def get_driver_id_or_fallback():
    """
    Obtiene el driver_id o devuelve un valor de respaldo.
    
    Returns:
        str: driver_id real o "unknown_driver"
    """
    driver_id = get_current_driver_id()
    if driver_id:
        return driver_id
    
    print("[WARNING] Usando driver_id de respaldo")
    return "unknown_driver"

def get_trip_id_or_fallback():
    """
    Obtiene el trip_id o devuelve un valor de respaldo.
    
    Returns:
        str: trip_id real o "unknown_trip"
    """
    trip_id = get_current_trip_id()
    if trip_id:
        return trip_id
    
    print("[WARNING] Usando trip_id de respaldo")
    return "unknown_trip"