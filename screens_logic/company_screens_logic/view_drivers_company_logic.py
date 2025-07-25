from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from database import get_drivers_by_company

class ViewDriversCompanyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drivers_data = []
    
    def on_enter(self):
        self.load_drivers()
    
    def load_drivers(self):
        try:
            current_user = App.get_running_app().current_user
            print(f"Usuario actual: {current_user}")
            
            if not current_user:
                print("Error: No hay sesión activa")
                return
            
            user_role = current_user.get('role')
            print(f"Rol del usuario: {user_role}")
            
            if user_role not in ['admin', 'company']:
                print(f"Error: El usuario no tiene permisos para ver conductores. Rol: {user_role}")
                return
            
            if user_role == 'admin':
                company_id = current_user.get('company_id')
            else:
                company_id = current_user.get('id')
            
            if not company_id:
                print("Error: No se pudo obtener el ID de la compañía")
                return
            
            print(f"Buscando conductores para company_id: {company_id}")
            self.drivers_data = get_drivers_by_company(company_id)
            print(f"Conductores obtenidos: {len(self.drivers_data)}")
            
            if self.drivers_data:
                for i, driver in enumerate(self.drivers_data[:3]):
                    print(f"  {i+1}. {driver.get('name', 'N/A')} - {driver.get('email', 'N/A')}")
            
            self.update_drivers_list()
            
        except Exception as e:
            print(f"Error al cargar conductores: {e}")
            import traceback
            traceback.print_exc()
            self.drivers_data = []
            self.update_drivers_list()
    
    def update_drivers_list(self):
        try:
            drivers_list = self.ids.drivers_list
            drivers_list.clear_widgets()
            
            if not self.drivers_data:
                drivers_list.add_widget(self.create_no_drivers_widget())
                return
            
            for driver in self.drivers_data:
                drivers_list.add_widget(self.create_driver_widget(driver))
                
        except Exception as e:
            print(f"Error al actualizar lista de conductores: {e}")
            import traceback
            traceback.print_exc()
    
    def create_no_drivers_widget(self):
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            padding=dp(20)
        )
        with container.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            container.rect = Rectangle(size=container.size, pos=container.pos)
        container.bind(size=self.update_rect, pos=self.update_rect)
        
        label = Label(
            text="No hay conductores registrados en esta compañía",
            font_size=32,
            halign='center',
            valign='middle',
            color=(0.5, 0.5, 0.5, 1)
        )
        container.add_widget(label)
        return container
    
    def create_driver_widget(self, driver):
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(15),
            spacing=dp(5)
        )
        with container.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            container.rect = Rectangle(size=container.size, pos=container.pos)
            Color(0.8, 0.8, 0.8, 1)
            container.border = Rectangle(size=container.size, pos=container.pos)
        container.bind(size=self.update_rect, pos=self.update_rect)
        
        info_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(2)
        )
        
        name_label = Label(
            text=f"Nombre: {driver.get('name', 'N/A')}",
            font_size=32,
            bold=True,
            halign='left',
            valign='middle',
            text_size=(None, None),
            size_hint_y=None,
            height=dp(25),
            color=(0, 0, 0, 1)
        )
        name_label.bind(size=name_label.setter('text_size'))
        
        email_label = Label(
            text=f"Email: {driver.get('email', 'N/A')}",
            font_size=32,
            halign='left',
            valign='middle',
            text_size=(None, None),
            size_hint_y=None,
            height=dp(25),
            color=(0, 0, 0, 1)
        )
        email_label.bind(size=email_label.setter('text_size'))
        
        info_container.add_widget(name_label)
        info_container.add_widget(email_label)
        
        button_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            padding=(dp(0), dp(10), dp(0), dp(0))
        )
        
        view_reports_btn = Button(
            text="Ver Viajes",
            size_hint_x=0.3,
            size_hint_y=None,
            height=dp(35),
            background_color=(0.2, 0.6, 0.86, 1),
            color=(0, 0, 0, 1),
            on_press=lambda x: self.view_driver_reports(driver['id'], driver['name'])
        )
        
        spacer = Label(size_hint_x=0.7)
        button_container.add_widget(spacer)
        button_container.add_widget(view_reports_btn)
        
        container.add_widget(info_container)
        container.add_widget(button_container)
        
        return container
    
    def update_rect(self, instance, value):
        if hasattr(instance, 'rect'):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
        if hasattr(instance, 'border'):
            instance.border.pos = instance.pos
            instance.border.size = instance.size

    def refresh_drivers(self):
        print("Actualizando lista de conductores...")
        self.load_drivers()

    def go_back(self):
        try:
            current_user = App.get_running_app().current_user
            if current_user:
                user_role = current_user.get('role')
                if user_role == 'admin':
                    self.manager.current = 'dashboard_admin'
                elif user_role == 'company':
                    self.manager.current = 'dashboard_company'
                else:
                    print(f"Rol no reconocido: {user_role}")
                    self.manager.current = 'login'
            else:
                print("No hay sesión activa")
                self.manager.current = 'login'
        except Exception as e:
            print(f"Error al regresar: {e}")
            self.manager.current = 'login'

    def view_driver_reports(self, driver_id, driver_name):
        try:
            app = App.get_running_app()
            app.selected_driver = {
                'id': driver_id,
                'name': driver_name
            }
            print(f"Navegando a reportes del conductor: {driver_name} (ID: {driver_id})")
            self.manager.current = 'view_trips_company'
        except Exception as e:
            print(f"Error al navegar a reportes: {e}")
            import traceback
            traceback.print_exc()
