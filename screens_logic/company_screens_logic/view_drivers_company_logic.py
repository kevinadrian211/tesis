from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.animation import Animation
from database import get_drivers_by_company

class ViewDriversCompanyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drivers_data = []
        # Colores del tema
        self.colors = {
            'background': (255/255, 252/255, 242/255, 1),  # #FFFCF2
            'surface': (204/255, 197/255, 185/255, 1),     # #CCC5B9
            'primary': (168/255, 159/255, 145/255, 1),     # #A89F91
            'border': (20/255, 26/255, 28/255, 1),         # #141A1C
            'text': (20/255, 26/255, 28/255, 1),           # #141A1C
            'text_secondary': (20/255, 26/255, 28/255, 0.7)
        }
    
    def on_enter(self):
        self.load_drivers()
        # Animación de entrada suave
        self.opacity = 0
        Animation(opacity=1, duration=0.3).start(self)
    
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
            
            for i, driver in enumerate(self.drivers_data):
                widget = self.create_driver_widget(driver)
                drivers_list.add_widget(widget)
                # Animación escalonada para cada elemento
                widget.opacity = 0
                Animation(opacity=1, duration=0.2, t='out_cubic').start(widget)
                
        except Exception as e:
            print(f"Error al actualizar lista de conductores: {e}")
            import traceback
            traceback.print_exc()
    
    def create_no_drivers_widget(self):
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(150),
            padding=dp(30),
            spacing=dp(15)
        )
        
        with container.canvas.before:
            Color(*self.colors['surface'])
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
        
        container.bind(size=self.update_canvas_rect, pos=self.update_canvas_rect)
        
        # Icono de conductor eliminado
        
        # Mensaje principal
        message_label = Label(
            text="No hay conductores registrados",
            font_size=sp(18),
            bold=True,
            halign='center',
            valign='middle',
            color=self.colors['text'],
            size_hint_y=None,
            height=dp(30)
        )
        
        # Submensaje
        sub_label = Label(
            text="Los conductores aparecerán aquí una vez registrados",
            font_size=sp(14),
            halign='center',
            valign='middle',
            color=self.colors['text_secondary'],
            size_hint_y=None,
            height=dp(25),
            italic=True
        )
        
        container.add_widget(message_label)
        container.add_widget(sub_label)
        
        return container
    
    def create_driver_widget(self, driver):
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(130),
            padding=dp(18),
            spacing=dp(10)
        )
        
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
        
        container.bind(size=self.update_canvas_rect, pos=self.update_canvas_rect)
        
        # Header del conductor
        header_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(35),
            spacing=dp(10)
        )
        
        # Información del conductor
        info_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(5)
        )
        
        name_label = Label(
            text=f"{driver.get('name', 'N/A')}",
            font_size=sp(18),
            bold=True,
            halign='left',
            valign='middle',
            text_size=(None, None),
            size_hint_y=None,
            height=dp(25),
            color=self.colors['text']
        )
        name_label.bind(size=name_label.setter('text_size'))
        
        email_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(20),
            spacing=dp(5)
        )
        
        email_label = Label(
            text=f"{driver.get('email', 'N/A')}",
            font_size=sp(15),
            halign='left',
            valign='middle',
            text_size=(None, None),
            color=self.colors['text_secondary']
        )
        email_label.bind(size=email_label.setter('text_size'))
        
        email_layout.add_widget(email_label)
        
        info_layout.add_widget(name_label)
        info_layout.add_widget(email_layout)
        
        header_layout.add_widget(info_layout)
        
        # Botón de acción
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(45),
            padding=[dp(0), dp(5), dp(0), dp(0)]
        )
        
        spacer = Label(size_hint_x=0.5)
        
        view_trips_btn = Button(
            text="Ver Viajes",
            size_hint_x=0.5,
            size_hint_y=None,
            height=dp(35),
            font_size=sp(14),
            bold=True,
            background_normal='',
            background_color=(0, 0, 0, 0),  # Transparente
            color=self.colors['text']
        )
        
        # Estilo personalizado para el botón
        with view_trips_btn.canvas.before:
            Color(*self.colors['primary'])
            view_trips_btn.bg_rect = RoundedRectangle(
                pos=view_trips_btn.pos,
                size=view_trips_btn.size,
                radius=[dp(20)]
            )
            Color(*self.colors['border'])
            view_trips_btn.border_line = Line(
                width=dp(1),
                rounded_rectangle=(
                    view_trips_btn.x, view_trips_btn.y, 
                    view_trips_btn.width, view_trips_btn.height, 
                    dp(20)
                )
            )
        
        view_trips_btn.bind(
            size=self.update_button_canvas,
            pos=self.update_button_canvas,
            on_press=lambda x: self.view_driver_reports(driver['id'], driver['name'])
        )
        
        # Efecto hover para botón
        def on_button_press(instance):
            # Cambiar el color del fondo del canvas
            with instance.canvas.before:
                Color(148/255, 139/255, 125/255, 1)  # Color más oscuro
                instance.bg_rect = RoundedRectangle(
                    pos=instance.pos,
                    size=instance.size,
                    radius=[dp(20)]
                )
                Color(*self.colors['border'])
                instance.border_line = Line(
                    width=dp(1),
                    rounded_rectangle=(
                        instance.x, instance.y, 
                        instance.width, instance.height, 
                        dp(20)
                    )
                )
        
        def on_button_release(instance):
            # Restaurar color original
            with instance.canvas.before:
                Color(*self.colors['primary'])
                instance.bg_rect = RoundedRectangle(
                    pos=instance.pos,
                    size=instance.size,
                    radius=[dp(20)]
                )
                Color(*self.colors['border'])
                instance.border_line = Line(
                    width=dp(1),
                    rounded_rectangle=(
                        instance.x, instance.y, 
                        instance.width, instance.height, 
                        dp(20)
                    )
                )
        
        view_trips_btn.bind(on_press=on_button_press, on_release=on_button_release)
        
        button_layout.add_widget(spacer)
        button_layout.add_widget(view_trips_btn)
        
        container.add_widget(header_layout)
        container.add_widget(button_layout)
        
        return container
    
    def update_canvas_rect(self, instance, value):
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
        if hasattr(instance, 'border_line'):
            instance.border_line.rounded_rectangle = (
                instance.x, instance.y, instance.width, instance.height, dp(12)
            )
    
    def update_button_canvas(self, instance, value):
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
        if hasattr(instance, 'border_line'):
            instance.border_line.rounded_rectangle = (
                instance.x, instance.y, instance.width, instance.height, dp(20)
            )

    def refresh_drivers(self):
        print("Actualizando lista de conductores...")
        # Animación de rotación para el botón de refresh
        refresh_btn = None
        for child in self.children[0].children:
            if hasattr(child, 'children'):
                for btn in child.children:
                    if hasattr(btn, 'text') and btn.text == "⟳":
                        refresh_btn = btn
                        break
        
        if refresh_btn:
            Animation(rotation=360, duration=0.5).start(refresh_btn)
            refresh_btn.rotation = 0
        
        self.load_drivers()

    def go_back(self):
        try:
            # Animación de salida
            Animation(opacity=0, duration=0.2).start(self)
            
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
            
            # Animación de salida
            Animation(opacity=0, duration=0.2).start(self)
            self.manager.current = 'view_trips_company'
            
        except Exception as e:
            print(f"Error al navegar a reportes: {e}")
            import traceback
            traceback.print_exc()