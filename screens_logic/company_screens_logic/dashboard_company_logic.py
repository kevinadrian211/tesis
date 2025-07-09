from kivy.uix.screenmanager import ScreenManager

# Función para registrar una compañía
def register_company(name, email, password):
    """
    Registra una nueva compañía y la redirige a la pantalla de dashboard.
    """
    try:
        # Aquí se asume que ya has registrado la compañía en la base de datos...
        # Simulamos el éxito de la operación
        response = {"status": "success", "company_id": "1234"}  # Respuesta de ejemplo

        if response['status'] == 'success':
            # Si la compañía se registró correctamente, redirigir al dashboard
            print(f"Compañía '{name}' registrada exitosamente.")
            # La redirección aquí se hace al cambiar la pantalla usando el ScreenManager
            return True
        else:
            print("Error al registrar la compañía.")
            return False
    except Exception as e:
        print(f"Ocurrió un error al intentar registrar la compañía: {e}")
        return False
