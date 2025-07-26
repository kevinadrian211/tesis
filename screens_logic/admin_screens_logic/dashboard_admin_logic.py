from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle, Line, RoundedRectangle
from kivy.animation import Animation
from database import get_drivers_by_company

class DashboardAdminScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drivers_data = []
        # Sistema de colores obligatorio
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
        Se ejecuta cuando se entra a la pantalla con animación
        """
        self.update_welcome_message()
        self.load_drivers()
        # Animación de entrada
        self.opacity = 0
        Animation(opacity=1, duration=0.3).start(self)
    
    def update_welcome_message(self):
        """
        Actualiza el mensaje de bienvenida con el nombre del admin
        """
        try:
            current_user = App.get_running_app().current_user
            if current_user and current_user.get('name'):
                welcome_text = f"Bienvenido, {current_user.get('name')}"
            else:
                welcome_text = "Bienvenido, Admin"
            
            # Actualizar el label de bienvenida
            if hasattr(self, 'ids') and 'welcome_label' in self.ids:
                self.ids.welcome_label.text = welcome_text
                
        except Exception as e:
            print(f"Error al actualizar mensaje de bienvenida: {e}")
    
    def load_drivers(self):
        """
        Carga los conductores de la compañía del administrador
        """
        try:
            # Obtener el usuario actual de la sesión
            current_user = App.get_running_app().current_user
            
            # Debug: Imprimir información de la sesión
            print(f"Usuario actual: {current_user}")
            
            if not current_user:
                print("Error: No hay sesión activa")
                return
            
            # Verificar si es admin
            user_role = current_user.get('role')
            print(f"Rol del usuario: {user_role}")
            
            if user_role != 'admin':
                print(f"Error: El usuario no es administrador. Rol: {user_role}")
                return
            
            # Obtener company_id del admin
            company_id = current_user.get('company_id')
            print(f"Admin - Company ID: {company_id}")
            
            if not company_id:
                print("Error: No se pudo obtener el ID de la compañía")
                return
            
            # Obtener conductores de la base de datos
            print(f"Buscando conductores para company_id: {company_id}")
            self.drivers_data = get_drivers_by_company(company_id)
            print(f"Conductores obtenidos: {len(self.drivers_data)}")
            
            # Debug: Imprimir primeros conductores
            if self.drivers_data:
                print("Primeros conductores:")
                for i, driver in enumerate(self.drivers_data[:3]):  # Solo los primeros 3
                    print(f"  {i+1}. {driver.get('name', 'N/A')} - {driver.get('email', 'N/A')}")
            
            # Actualizar la interfaz
            self.update_drivers_list()
            
        except Exception as e:
            print(f"Error al cargar conductores: {e}")
            import traceback
            traceback.print_exc()
            self.drivers_data = []
            self.update_drivers_list()
    
    def update_drivers_list(self):
        """
        Actualiza la lista visual de conductores
        """
        try:
            # Limpiar la lista actual
            drivers_list = self.ids.drivers_list
            drivers_list.clear_widgets()
            
            if not self.drivers_data:
                # Si no hay conductores, mostrar mensaje
                no_drivers_widget = self.create_no_drivers_widget()
                drivers_list.add_widget(no_drivers_widget)
                return
            
            # Crear widgets para cada conductor
            for driver in self.drivers_data:
                driver_widget = self.create_driver_widget(driver)
                drivers_list.add_widget(driver_widget)
                
        except Exception as e:
            print(f"Error al actualizar lista de conductores: {e}")
            import traceback
            traceback.print_exc()
    
    def create_no_drivers_widget(self):
        """
        Crea un widget para mostrar cuando no hay conductores
        """
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(20),
            spacing=dp(10)
        )
        
        # Canvas personalizado con colores del sistema
        with container.canvas.before:
            Color(*self.colors['background'])
            container.bg_rect = RoundedRectangle(
                size=container.size,
                pos=container.pos,
                radius=[dp(12)]
            )
            Color(*self.colors['border'])
            container.border_line = Line(
                width=dp(1),
                rounded_rectangle=(container.x, container.y, container.width, container.height, dp(12))
            )
        
        # Actualizar canvas cuando cambie el tamaño
        container.bind(size=self.update_canvas_rect, pos=self.update_canvas_rect)
        
        message_label = Label(
            text="No hay conductores registrados en esta compañía",
            font_size=sp(16),
            halign='center',
            valign='middle',
            color=self.colors['text'],
            text_size=(None, None)
        )
        message_label.bind(size=message_label.setter('text_size'))
        
        container.add_widget(message_label)
        return container
    
    def create_driver_widget(self, driver):
        """
        Crea un widget para mostrar información básica de un conductor
        """
        # Contenedor principal con diseño profesional
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(130),
            padding=dp(18),
            spacing=dp(10)
        )
        
        # Canvas personalizado con sistema de colores
        with container.canvas.before:
            Color(*self.colors['background'])
            container.bg_rect = RoundedRectangle(
                size=container.size,
                pos=container.pos,
                radius=[dp(12)]
            )
            Color(*self.colors['border'])
            container.border_line = Line(
                width=dp(1),
                rounded_rectangle=(container.x, container.y, container.width, container.height, dp(12))
            )
        
        # Bind para actualizar canvas dinámicamente
        container.bind(size=self.update_canvas_rect, pos=self.update_canvas_rect)
        
        # Contenedor para la información del conductor
        info_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(5)
        )
        
        # Nombre del conductor con tipografía profesional
        name_label = Label(
            text=f"Nombre: {driver.get('name', 'N/A')}",
            font_size=sp(16),
            bold=True,
            halign='left',
            valign='middle',
            text_size=(None, None),
            size_hint_y=None,
            height=dp(30),
            color=self.colors['text']
        )
        name_label.bind(size=name_label.setter('text_size'))
        
        # Email del conductor
        email_label = Label(
            text=f"Email: {driver.get('email', 'N/A')}",
            font_size=sp(14),
            halign='left',
            valign='middle',
            text_size=(None, None),
            size_hint_y=None,
            height=dp(25),
            color=self.colors['text_secondary']
        )
        email_label.bind(size=email_label.setter('text_size'))
        
        # Agregar labels al contenedor de información
        info_container.add_widget(name_label)
        info_container.add_widget(email_label)
        
        # Contenedor para el botón
        button_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            padding=(dp(0), dp(5), dp(0), dp(0))
        )
        
        # Botón profesional para ver reportes
        view_reports_btn = Button(
            text="Ver Reportes",
            font_size=sp(12),
            bold=True,
            size_hint_x=0.35,
            size_hint_y=None,
            height=dp(35),
            background_color=(0, 0, 0, 0),  # Fondo transparente
            color=self.colors['text'],
            on_press=lambda x: self.view_driver_reports(driver['id'], driver['name'])
        )
        
        # Canvas personalizado para el botón
        with view_reports_btn.canvas.before:
            Color(*self.colors['primary'])
            view_reports_btn.bg_rect = RoundedRectangle(
                size=view_reports_btn.size,
                pos=view_reports_btn.pos,
                radius=[dp(8)]
            )
            Color(*self.colors['border'])
            view_reports_btn.border_line = Line(
                width=dp(1),
                rounded_rectangle=(view_reports_btn.x, view_reports_btn.y, 
                                 view_reports_btn.width, view_reports_btn.height, dp(8))
            )
        
        # Función para actualizar el canvas del botón
        def update_btn_canvas(instance, value):
            if hasattr(instance, 'bg_rect'):
                instance.bg_rect.pos = instance.pos
                instance.bg_rect.size = instance.size
            if hasattr(instance, 'border_line'):
                instance.border_line.rounded_rectangle = (
                    instance.x, instance.y, instance.width, instance.height, dp(8)
                )
        
        # Bind para actualizar el canvas del botón
        view_reports_btn.bind(pos=update_btn_canvas, size=update_btn_canvas)
        
        # Espaciador para alinear el botón a la derecha
        spacer = Label(size_hint_x=0.65)
        
        button_container.add_widget(spacer)
        button_container.add_widget(view_reports_btn)
        
        # Agregar contenedores al contenedor principal
        container.add_widget(info_container)
        container.add_widget(button_container)
        
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
                instance.x, instance.y, instance.width, instance.height, dp(12)
            )

    def view_driver_reports(self, driver_id, driver_name):
        """
        Navega a la pantalla de reportes del conductor seleccionado
        """
        try:
            # Crear objeto de datos del conductor
            driver_data = {
                'id': driver_id,
                'name': driver_name
            }
            
            # Guardar el conductor seleccionado en la app
            app = App.get_running_app()
            app.selected_driver = driver_data
            
            print(f"Navegando a reportes del conductor: {driver_name} (ID: {driver_id})")
            
            # Cambiar a la pantalla de reportes
            self.manager.current = 'view_trips_admin'
            
        except Exception as e:
            print(f"Error al navegar a reportes: {e}")
            import traceback
            traceback.print_exc()
    
    def logout(self):
        """
        Cierra la sesión del administrador
        """
        try:
            # Limpiar la sesión
            App.get_running_app().current_user = None
            
            # Navegar al login
            self.manager.current = 'login'
            
        except Exception as e:
            print(f"Error al cerrar sesión: {e}")
            self.manager.current = 'login'