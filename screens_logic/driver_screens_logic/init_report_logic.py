from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.lang import Builder
from database import create_trip

# Cargar el archivo KV correspondiente
Builder.load_file("screens/driver_screens/init_report.kv")

class ReportScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_trip = None  # Para guardar el viaje actual
    
    def on_enter(self):
        """
        Este método se ejecuta cuando se entra en la pantalla.
        Aquí podemos mostrar información del usuario actual.
        """
        app = App.get_running_app()
        if hasattr(app, 'current_user') and app.current_user:
            user = app.current_user
            if user.get('role') == 'driver':
                self.ids.driver_name_label.text = f"Conductor: {user.get('name', 'N/A')}"
                print(f"Usuario actual: {user}")
            else:
                print("Usuario no es conductor")
        else:
            print("No hay usuario actual")
    
    def validate_trip_data(self):
        """
        Valida que los campos obligatorios estén completos
        """
        start_location = self.ids.start_location_input.text.strip()
        end_location = self.ids.end_location_input.text.strip()
        
        if not start_location or not end_location:
            self.ids.status_label.text = "Error: Todos los campos son obligatorios"
            return False
        
        return True
    
    def create_new_trip(self):
        """
        Crea un nuevo viaje en la base de datos
        """
        if not self.validate_trip_data():
            return False
        
        app = App.get_running_app()
        if not hasattr(app, 'current_user') or not app.current_user:
            self.ids.status_label.text = "Error: No hay usuario activo"
            return False
        
        user = app.current_user
        if user.get('role') != 'driver':
            self.ids.status_label.text = "Error: Solo los conductores pueden crear viajes"
            return False
        
        # Capturar datos del formulario
        start_location = self.ids.start_location_input.text.strip()
        end_location = self.ids.end_location_input.text.strip()
        driver_id = user.get('id')
        company_id = user.get('company_id')
        
        # Crear el viaje en la base de datos
        trip_data = create_trip(driver_id, company_id, start_location, end_location)
        
        if trip_data:
            self.current_trip = trip_data
            # Guardar el viaje actual en la aplicación para uso posterior
            app.current_trip = trip_data
            
            self.ids.status_label.text = f"Viaje creado exitosamente (ID: {trip_data['id'][:8]}...)"
            print(f"Viaje creado: {trip_data}")
            return True
        else:
            self.ids.status_label.text = "Error: No se pudo crear el viaje"
            return False
    
    def on_start_trip(self):
        """
        Maneja el inicio del viaje
        """
        # Primero crear el viaje si no existe
        if not self.current_trip:
            if not self.create_new_trip():
                return
        
        # Cambiar el estado y navegar a monitoring
        self.ids.status_label.text = "Estado: Viaje iniciado"
        print(f"Iniciando viaje con ID: {self.current_trip['id']}")
        
        # Navegar a la pantalla de monitoreo
        self.manager.current = "monitoring"
    
    def go_back(self):
        """
        Navega de vuelta al dashboard del conductor
        """
        self.manager.current = "dashboard_driver"