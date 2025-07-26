from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.uix.boxlayout import BoxLayout
from database import create_trip

# Cargar el archivo KV correspondiente
Builder.load_file("screens/driver_screens/init_report.kv")

class ReportScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_trip = None  # Para guardar el viaje actual
        
        # Sistema de colores profesional
        self.colors = {
            'background': (255/255, 252/255, 242/255, 1),  # #FFFCF2
            'surface': (204/255, 197/255, 185/255, 1),     # #CCC5B9
            'primary': (168/255, 159/255, 145/255, 1),     # #A89F91
            'border': (20/255, 26/255, 28/255, 1),         # #141A1C
            'text': (20/255, 26/255, 28/255, 1),           # #141A1C
            'text_secondary': (20/255, 26/255, 28/255, 0.7)
        }
    
    def on_enter(self):
        """
        Este método se ejecuta cuando se entra en la pantalla.
        Incluye animación de entrada y carga de datos.
        """
        # Animación de entrada profesional
        self.opacity = 0
        Animation(opacity=1, duration=0.3).start(self)
        
        # Cargar datos del usuario
        self.load_user_data()
    
    def load_user_data(self):
        """
        Carga y muestra información del usuario actual
        """
        app = App.get_running_app()
        if hasattr(app, 'current_user') and app.current_user:
            user = app.current_user
            if user.get('role') == 'driver':
                self.ids.driver_name_label.text = f"Conductor: {user.get('name', 'N/A')}"
                print(f"Usuario actual: {user}")
            else:
                print("Usuario no es conductor")
                self.ids.status_label.text = "Error: Usuario no es conductor"
        else:
            print("No hay usuario actual")
            self.ids.status_label.text = "Error: No hay sesión activa"
    
    def create_input_widget(self, label_text, hint_text, input_id):
        """
        Crea un widget de entrada con canvas personalizado
        """
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(80),
            spacing=dp(8)
        )
        
        # Aplicar canvas personalizado
        with container.canvas.before:
            Color(*self.colors['surface'])
            container.bg_rect = RoundedRectangle(
                size=container.size, 
                pos=container.pos, 
                radius=[dp(8)]
            )
            Color(*self.colors['border'])
            container.border_line = Line(
                width=dp(1),
                rounded_rectangle=(container.x, container.y, container.width, container.height, dp(8))
            )
        
        container.bind(size=self.update_canvas_rect, pos=self.update_canvas_rect)
        return container
    
    def update_canvas_rect(self, instance, value):
        """
        Actualiza el canvas cuando cambia el tamaño o posición
        """
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
        if hasattr(instance, 'border_line'):
            instance.border_line.rounded_rectangle = (
                instance.x, instance.y, instance.width, instance.height, dp(8)
            )
    
    def validate_trip_data(self):
        """
        Valida que los campos obligatorios estén completos
        """
        start_location = self.ids.start_location_input.text.strip()
        end_location = self.ids.end_location_input.text.strip()
        
        if not start_location or not end_location:
            self.ids.status_label.text = "Estado: Campos obligatorios vacíos"
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
            self.ids.status_label.text = "Estado: Error - Sin usuario activo"
            return False
        
        user = app.current_user
        if user.get('role') != 'driver':
            self.ids.status_label.text = "Estado: Error - Acceso denegado"
            return False
        
        # Mostrar estado de carga
        self.ids.status_label.text = "Estado: Creando viaje..."
        
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
            trip_id_short = trip_data['id'][:8] if len(trip_data['id']) > 8 else trip_data['id']
            self.ids.status_label.text = f"Estado: Viaje creado (ID: {trip_id_short})"
            print(f"Viaje creado: {trip_data}")
            return True
        else:
            self.ids.status_label.text = "Estado: Error - No se pudo crear el viaje"
            return False
    
    def on_start_trip(self):
        """
        Maneja el inicio del viaje con validaciones
        """
        # Primero crear el viaje si no existe
        if not self.current_trip:
            if not self.create_new_trip():
                return
        
        # Animación de transición
        self.ids.status_label.text = "Estado: Iniciando viaje..."
        
        # Pequeña pausa para mostrar el estado
        def navigate_to_monitoring(dt):
            print(f"Iniciando viaje con ID: {self.current_trip['id']}")
            self.manager.current = "monitoring"
        
        from kivy.clock import Clock
        Clock.schedule_once(navigate_to_monitoring, 0.5)
    
    def on_logout(self):
        """
        Maneja el cierre de sesión con limpieza completa
        """
        # Animación de salida
        self.ids.status_label.text = "Estado: Cerrando sesión..."
        
        app = App.get_running_app()
        
        # Limpiar datos del usuario actual
        if hasattr(app, 'current_user'):
            app.current_user = None
        
        # Limpiar viaje actual si existe
        if hasattr(app, 'current_trip'):
            app.current_trip = None
        
        # Limpiar datos locales de la pantalla
        self.current_trip = None
        
        # Limpiar campos del formulario
        self.ids.start_location_input.text = ""
        self.ids.end_location_input.text = ""
        
        # Actualizar labels
        self.ids.driver_name_label.text = "Conductor: Sin sesión"
        
        print("Sesión cerrada exitosamente")
        
        # Navegar con pequeña pausa para mostrar estado
        def navigate_to_login(dt):
            self.manager.current = "login"
        
        from kivy.clock import Clock
        Clock.schedule_once(navigate_to_login, 0.3)
    
    def clear_form(self):
        """
        Limpia todos los campos del formulario
        """
        self.ids.start_location_input.text = ""
        self.ids.end_location_input.text = ""
        self.ids.status_label.text = "Estado: Formulario limpiado"