from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from database import get_drivers_by_company

class DashboardAdminScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drivers_data = []
    
    def on_enter(self):
        """
        Se ejecuta cuando se entra a la pantalla
        """
        self.update_welcome_message()
        self.load_drivers()
    
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
            height=dp(100),
            padding=dp(20)
        )
        
        # Crear fondo con color
        with container.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Gris claro
            container.rect = Rectangle(size=container.size, pos=container.pos)
        
        # Actualizar el rectángulo cuando cambie el tamaño
        container.bind(size=self.update_rect, pos=self.update_rect)
        
        message_label = Label(
            text="No hay conductores registrados en esta compañía",
            font_size=16,
            halign='center',
            valign='middle',
            color=(0.5, 0.5, 0.5, 1)
        )
        
        container.add_widget(message_label)
        return container
    
    def create_driver_widget(self, driver):
        """
        Crea un widget para mostrar información básica de un conductor
        """
        # Contenedor principal con fondo
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(15),
            spacing=dp(5)
        )
        
        # Crear fondo con borde
        with container.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Fondo gris muy claro
            container.rect = Rectangle(size=container.size, pos=container.pos)
            Color(0.8, 0.8, 0.8, 1)  # Borde gris
            container.border = Rectangle(size=container.size, pos=container.pos)
        
        # Actualizar el rectángulo cuando cambie el tamaño
        container.bind(size=self.update_rect, pos=self.update_rect)
        
        # Contenedor para la información del conductor
        info_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(2)
        )
        
        # Nombre del conductor
        name_label = Label(
            text=f"Nombre: {driver.get('name', 'N/A')}",
            font_size=16,
            bold=True,
            halign='left',
            valign='middle',
            text_size=(None, None),
            size_hint_y=None,
            height=dp(25)
        )
        name_label.bind(size=name_label.setter('text_size'))
        
        # Email del conductor
        email_label = Label(
            text=f"Email: {driver.get('email', 'N/A')}",
            font_size=14,
            halign='left',
            valign='middle',
            text_size=(None, None),
            size_hint_y=None,
            height=dp(25),
            color=(0.6, 0.6, 0.6, 1)
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
            padding=(dp(0), dp(10), dp(0), dp(0))
        )
        
        # Botón para ver reportes
        view_reports_btn = Button(
            text="Ver Reportes",
            size_hint_x=0.3,
            size_hint_y=None,
            height=dp(35),
            background_color=(0.2, 0.6, 0.86, 1),  # Color azul
            on_press=lambda x: self.view_driver_reports(driver['id'], driver['name'])
        )
        
        # Espaciador para alinear el botón a la derecha
        spacer = Label(size_hint_x=0.7)
        
        button_container.add_widget(spacer)
        button_container.add_widget(view_reports_btn)
        
        # Agregar contenedores al contenedor principal
        container.add_widget(info_container)
        container.add_widget(button_container)
        
        return container
    
    def update_rect(self, instance, value):
        """
        Actualiza el rectángulo de fondo cuando cambia el tamaño del widget
        """
        if hasattr(instance, 'rect'):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
        if hasattr(instance, 'border'):
            instance.border.pos = instance.pos
            instance.border.size = instance.size

    def refresh_drivers(self):
        """
        Actualiza la lista de conductores
        """
        print("Actualizando lista de conductores...")
        self.load_drivers()

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
            self.manager.current = 'view_reports_admin'
            
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