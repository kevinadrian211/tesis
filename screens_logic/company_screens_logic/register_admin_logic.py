from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.metrics import dp
from database import register_admin  # Asegúrate de que esta función esté importada correctamente

class RegisterAdminScreen(Screen):
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
        """Animación de entrada profesional"""
        self.opacity = 0
        Animation(opacity=1, duration=0.3).start(self)
        
        # Limpiar campos al entrar
        self.clear_fields()
    
    def register_admin(self):
        """Registra un nuevo administrador con validaciones profesionales"""
        try:
            # Obtener datos de los campos
            name = self.ids.admin_name.text.strip()
            email = self.ids.admin_email.text.strip()
            password = self.ids.admin_password.text.strip()
            confirm_password = self.ids.admin_confirm_password.text.strip()
            
            # Validaciones de campos vacíos
            if not name or not email or not password or not confirm_password:
                self.show_modern_popup("Error", "Todos los campos son obligatorios.")
                return
            
            # Validación de nombre (mínimo 3 caracteres)
            if len(name) < 3:
                self.show_modern_popup("Error", "El nombre debe tener al menos 3 caracteres.")
                return
            
            # Validación básica de email
            if "@" not in email or "." not in email:
                self.show_modern_popup("Error", "Ingrese un correo electrónico válido.")
                return
            
            # Validación de contraseña
            if len(password) < 6:
                self.show_modern_popup("Error", "La contraseña debe tener al menos 6 caracteres.")
                return
            
            # Verificar que las contraseñas coincidan
            if password != confirm_password:
                self.show_modern_popup("Error", "Las contraseñas no coinciden.")
                return
            
            # Obtener el ID de la compañía desde el current_user
            app = App.get_running_app()
            current_user = getattr(app, 'current_user', None)
            
            if not current_user or current_user.get("role") != "company":
                self.show_modern_popup("Error", "No se ha identificado a la compañía.")
                return
            
            company_id = current_user.get("id")
            
            # Mostrar feedback visual durante el registro
            self.show_loading_state(True)
            
            # Registrar el administrador en Supabase
            success = register_admin(name, email, password, company_id)
            
            self.show_loading_state(False)
            
            if success:
                self.clear_fields()
                self.show_success_popup("Éxito", "Administrador registrado correctamente.")
                # Navegar de vuelta al dashboard después de un breve delay
                Animation(opacity=0.7, duration=0.2).start(self)
                self.manager.current = "dashboard_company"
            else:
                self.show_modern_popup("Error", "No se pudo registrar el administrador. Verifica que el email no esté en uso.")
                
        except Exception as e:
            self.show_loading_state(False)
            print(f"Error al registrar administrador: {e}")
            self.show_modern_popup("Error", "Ocurrió un error inesperado. Intente nuevamente.")
    
    def show_modern_popup(self, title, message):
        """Popup moderno con estilo profesional"""
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(20)
        )
        
        # Mensaje
        message_label = Label(
            text=message,
            font_size=dp(14),
            color=self.colors['text'],
            halign='center',
            valign='middle',
            text_size=(None, None),
            size_hint_y=0.7
        )
        message_label.bind(size=message_label.setter('text_size'))
        
        # Botón OK
        ok_button = Button(
            text="Entendido",
            size_hint=(0.6, None),
            height=dp(45),
            pos_hint={'center_x': 0.5},
            background_color=(0, 0, 0, 0),
            color=self.colors['text'],
            font_size=dp(12),
            bold=True
        )
        
        # Canvas personalizado para el botón
        with ok_button.canvas.before:
            Color(*self.colors['primary'])
            ok_button.bg_rect = RoundedRectangle(
                size=ok_button.size,
                pos=ok_button.pos,
                radius=[dp(8)]
            )
            Color(*self.colors['border'])
            ok_button.border_line = Line(
                width=dp(1),
                rounded_rectangle=(ok_button.x, ok_button.y, ok_button.width, ok_button.height, dp(8))
            )
        
        ok_button.bind(size=self.update_popup_button_canvas, pos=self.update_popup_button_canvas)
        
        content.add_widget(message_label)
        content.add_widget(ok_button)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.85, 0.35),
            title_size=dp(16),
            title_color=self.colors['text'],
            background_color=self.colors['surface'],
            separator_color=self.colors['border']
        )
        
        ok_button.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_success_popup(self, title, message):
        """Popup de éxito con estilo verde"""
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(20)
        )
        
        message_label = Label(
            text=message,
            font_size=dp(14),
            color=(0.2, 0.6, 0.2, 1),  # Verde
            halign='center',
            valign='middle',
            text_size=(None, None),
            size_hint_y=0.7,
            bold=True
        )
        message_label.bind(size=message_label.setter('text_size'))
        
        content.add_widget(message_label)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.85, 0.25),
            title_size=dp(16),
            title_color=(0.2, 0.6, 0.2, 1),
            background_color=self.colors['surface'],
            separator_color=self.colors['border'],
            auto_dismiss=True
        )
        
        popup.open()
        # Auto cerrar después de 2 segundos
        Animation(opacity=0, duration=0.5).start(popup)
    
    def update_popup_button_canvas(self, instance, value):
        """Actualiza el canvas de los botones del popup"""
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
        if hasattr(instance, 'border_line'):
            instance.border_line.rounded_rectangle = (
                instance.x, instance.y, instance.width, instance.height, dp(8)
            )
    
    def show_loading_state(self, loading):
        """Muestra estado de carga durante el registro"""
        register_button = None
        try:
            # Buscar el botón de registro en la interfaz
            for widget in self.walk():
                if hasattr(widget, 'text') and widget.text == "Registrar Administrador":
                    register_button = widget
                    break
            
            if register_button:
                if loading:
                    register_button.text = "Registrando..."
                    register_button.disabled = True
                else:
                    register_button.text = "Registrar Administrador" 
                    register_button.disabled = False
                    
        except Exception as e:
            print(f"Error al mostrar estado de carga: {e}")
    
    def clear_fields(self):
        """Limpia todos los campos del formulario"""
        try:
            self.ids.admin_name.text = ""
            self.ids.admin_email.text = ""
            self.ids.admin_password.text = ""
            self.ids.admin_confirm_password.text = ""
        except Exception as e:
            print(f"Error al limpiar campos: {e}")
    
    def validate_email(self, email):
        """Validación más robusta de email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def create_input_widget(self, label_text, input_id, hint_text, is_password=False):
        """Crea widgets de input con estilo personalizado (función helper)"""
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(75),
            spacing=dp(5)
        )
        
        # Label
        label = Label(
            text=label_text,
            font_size=dp(12),
            color=self.colors['text'],
            bold=True,
            halign='left',
            valign='bottom',
            text_size=(None, None),
            size_hint_y=None,
            height=dp(20)
        )
        
        # TextInput con canvas personalizado
        text_input = TextInput(
            hint_text=hint_text,
            multiline=False,
            password=is_password,
            font_size=dp(14),
            foreground_color=self.colors['text'],
            background_color=self.colors['background'], 
            size_hint_y=None,
            height=dp(50),
            padding=[dp(15), dp(12)]
        )
        
        # Canvas personalizado para el TextInput
        with text_input.canvas.before:
            Color(*self.colors['background'])
            text_input.bg_rect = RoundedRectangle(
                size=text_input.size,
                pos=text_input.pos,
                radius=[dp(8)]
            )
            Color(*self.colors['border'])
            text_input.border_line = Line(
                width=dp(1),
                rounded_rectangle=(text_input.x, text_input.y, text_input.width, text_input.height, dp(8))
            )
        
        text_input.bind(size=self.update_input_canvas, pos=self.update_input_canvas)
        
        container.add_widget(label)
        container.add_widget(text_input)
        
        return container
    
    def update_input_canvas(self, instance, value):
        """Actualiza el canvas de los TextInput"""
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
        if hasattr(instance, 'border_line'):
            instance.border_line.rounded_rectangle = (
                instance.x, instance.y, instance.width, instance.height, dp(8)
            )