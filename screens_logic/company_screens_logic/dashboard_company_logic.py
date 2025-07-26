from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.metrics import dp

class DashboardCompanyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
        """Animación de entrada y actualización de datos"""
        self.update_welcome_message()
        self.opacity = 0
        Animation(opacity=1, duration=0.3).start(self)
    
    def update_welcome_message(self):
        """Actualiza el mensaje de bienvenida personalizado"""
        try:
            current_user = App.get_running_app().current_user
            if current_user and current_user.get('name'):
                welcome_text = f"Bienvenido, {current_user.get('name')}"
            else:
                welcome_text = "Bienvenido, Compañía"
            
            # Actualizar el label si existe
            if hasattr(self, 'ids') and 'welcome_label' in self.ids:
                self.ids.welcome_label.text = welcome_text
        except Exception as e:
            print(f"Error al actualizar mensaje de bienvenida: {e}")
    
    def create_header_button(self, text, callback):
        """Crea botones del header con estilo personalizado"""
        from kivy.uix.button import Button
        
        button = Button(
            text=text,
            size_hint=(None, None),
            size=(dp(120), dp(40)),
            background_color=(0, 0, 0, 0),  # Transparente
            color=self.colors['text'],
            font_size=dp(12),
            bold=True
        )
        
        # Canvas personalizado para el botón
        with button.canvas.before:
            Color(*self.colors['surface'])
            button.bg_rect = RoundedRectangle(
                size=button.size,
                pos=button.pos,
                radius=[dp(8)]
            )
            Color(*self.colors['border'])
            button.border_line = Line(
                width=dp(1),
                rounded_rectangle=(button.x, button.y, button.width, button.height, dp(8))
            )
        
        # Bind para actualizar canvas cuando cambie posición/tamaño
        button.bind(size=self.update_button_canvas, pos=self.update_button_canvas)
        button.bind(on_press=callback)
        
        return button
    
    def create_main_button(self, text, callback):
        """Crea botones principales con estilo personalizado"""
        from kivy.uix.button import Button
        
        button = Button(
            text=text,
            size_hint=(0.8, None),
            height=dp(55),
            pos_hint={'center_x': 0.5},
            background_color=(0, 0, 0, 0),  # Transparente
            color=self.colors['text'],
            font_size=dp(14),
            bold=True
        )
        
        # Canvas personalizado para el botón
        with button.canvas.before:
            Color(*self.colors['primary'])
            button.bg_rect = RoundedRectangle(
                size=button.size,
                pos=button.pos,
                radius=[dp(12)]
            )
            Color(*self.colors['border'])
            button.border_line = Line(
                width=dp(1),
                rounded_rectangle=(button.x, button.y, button.width, button.height, dp(12))
            )
        
        # Bind para actualizar canvas
        button.bind(size=self.update_button_canvas, pos=self.update_button_canvas)
        button.bind(on_press=callback)
        
        return button
    
    def update_button_canvas(self, instance, value):
        """Actualiza el canvas de los botones cuando cambian posición/tamaño"""
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
        if hasattr(instance, 'border_line'):
            # Determinar el radio según el tipo de botón
            radius = dp(12) if instance.height > dp(50) else dp(8)
            instance.border_line.rounded_rectangle = (
                instance.x, instance.y, instance.width, instance.height, radius
            )
    
    def create_info_container(self):
        """Crea el contenedor de información con estilo personalizado"""
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(140),
            padding=dp(20),
            spacing=dp(10)
        )
        
        # Canvas personalizado para el contenedor
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
        
        # Labels con estilo personalizado
        title_label = Label(
            text="Panel de Empresa",
            font_size=dp(20),
            color=self.colors['text'],
            bold=True,
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(60)
        )
        
        subtitle_label = Label(
            text="Gestión de Conductores y Administradores",
            font_size=dp(14),
            color=self.colors['text_secondary'],
            halign='center',
            valign='middle',
            text_size=(None, None),
            size_hint_y=None,
            height=dp(50)
        )
        
        container.add_widget(title_label)
        container.add_widget(subtitle_label)
        
        # Bind para actualizar canvas
        container.bind(size=self.update_container_canvas, pos=self.update_container_canvas)
        
        return container
    
    def update_container_canvas(self, instance, value):
        """Actualiza el canvas de los contenedores"""
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
        if hasattr(instance, 'border_line'):
            instance.border_line.rounded_rectangle = (
                instance.x, instance.y, instance.width, instance.height, dp(12)
            )
    
    def ver_reportes(self, *args):
        """Navega a la pantalla de visualización de conductores"""
        # Animación de salida suave
        anim = Animation(opacity=0.7, duration=0.2)
        anim.bind(on_complete=lambda *x: setattr(self, 'opacity', 1))
        anim.start(self)
        
        self.manager.current = "view_drivers_company"
    
    def agregar_administrador(self, *args):
        """Navega a la pantalla de registro de administrador"""
        # Animación de salida suave
        anim = Animation(opacity=0.7, duration=0.2)
        anim.bind(on_complete=lambda *x: setattr(self, 'opacity', 1))
        anim.start(self)
        
        self.manager.current = "register_admin"
    
    def cerrar_sesion(self, *args):
        """Cierra la sesión y regresa al login"""
        try:
            app = App.get_running_app()
            # Limpiar toda la sesión
            app.clear_sessions()
            app.current_user = None
            print("Sesión cerrada correctamente.")
            
            # Animación de salida antes de cambiar de pantalla
            anim = Animation(opacity=0, duration=0.3)
            anim.bind(on_complete=self._navigate_to_login)
            anim.start(self)
            
        except Exception as e:
            print(f"Error al cerrar sesión desde dashboard de empresa: {e}")
            self.manager.current = "login"
    
    def _navigate_to_login(self, *args):
        """Navega al login después de la animación"""
        self.manager.current = "login"