from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.clock import Clock
from database import register_company, register_driver, register_admin, get_all_companies
import re

class RegisterScreen(Screen):
    account_type = StringProperty("")
    company_name = StringProperty("")
    driver_name = StringProperty("")
    driver_email = StringProperty("")
    driver_password = StringProperty("")
    company_email = StringProperty("")
    company_password = StringProperty("")
    company_id = StringProperty("")
    company_password_confirm = StringProperty("")
    driver_password_confirm = StringProperty("")
    admin_password_confirm = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.colors = {
            'background': (255/255, 252/255, 242/255, 1),  # #FFFCF2
            'surface': (204/255, 197/255, 185/255, 1),     # #CCC5B9
            'primary': (168/255, 159/255, 145/255, 1),     # #A89F91
            'border': (20/255, 26/255, 28/255, 1),         # #141A1C
            'text': (20/255, 26/255, 28/255, 1),           # #141A1C
            'text_secondary': (20/255, 26/255, 28/255, 0.7)
        }
        self._bindings_setup = False

    def on_enter(self):
        """Método ejecutado al entrar en la pantalla."""
        print(f"Llegaste como: {self.account_type}")
        
        # Animación de entrada
        self.opacity = 0
        Animation(opacity=1, duration=0.3).start(self)
        
        # Configurar interfaz después de un pequeño delay para asegurar que los widgets estén listos
        Clock.schedule_once(self._setup_interface, 0.1)

    def _setup_interface(self, dt):
        """Configura la interfaz después de que los widgets estén listos."""
        # Limpiar campos y configurar interfaz según el tipo de cuenta
        if self.account_type == "company":
            self.clear_fields_for_driver()
            print("Campos de Company visibles.")
        elif self.account_type == "driver":
            self.clear_fields_for_company()
            print("Campos de Driver visibles.")
        elif self.account_type == "admin":
            self.clear_fields_for_company()
            print("Campos de Admin visibles.")
        
        # Configurar bindings para los TextInputs
        self.setup_text_bindings()
        
        # Limpiar el indicador de estado de contraseñas
        self.update_password_status()

    def setup_text_bindings(self):
        """Configura los bindings bidireccionales para los TextInputs."""
        if self._bindings_setup:
            return  # Evitar configurar múltiples veces
            
        try:
            # Company fields - Solo si es tipo company
            if self.account_type == "company":
                company_name_input = self.ids.get('company_name_input')
                if company_name_input:
                    company_name_input.bind(text=self.on_company_name_change)
                    
                company_email_input = self.ids.get('company_email_input')
                if company_email_input:
                    company_email_input.bind(text=self.on_company_email_change)
                    
                company_password_input = self.ids.get('company_password_input')
                if company_password_input:
                    company_password_input.bind(text=self.on_company_password_change)
                    
                company_password_confirm_input = self.ids.get('company_password_confirm_input')
                if company_password_confirm_input:
                    company_password_confirm_input.bind(text=self.on_company_password_confirm_change)
            
            # Driver fields - Solo si es tipo driver
            elif self.account_type == "driver":
                driver_name_input = self.ids.get('driver_name_input')
                if driver_name_input:
                    driver_name_input.bind(text=self.on_driver_name_change)
                    
                driver_email_input = self.ids.get('driver_email_input')
                if driver_email_input:
                    driver_email_input.bind(text=self.on_driver_email_change)
                    
                driver_password_input = self.ids.get('driver_password_input')
                if driver_password_input:
                    driver_password_input.bind(text=self.on_driver_password_change)
                    
                driver_password_confirm_input = self.ids.get('driver_password_confirm_input')
                if driver_password_confirm_input:
                    driver_password_confirm_input.bind(text=self.on_driver_password_confirm_change)
            
            # Admin fields - Solo si es tipo admin
            elif self.account_type == "admin":
                admin_name_input = self.ids.get('admin_name_input')
                if admin_name_input:
                    admin_name_input.bind(text=self.on_admin_name_change)
                    
                admin_email_input = self.ids.get('admin_email_input')
                if admin_email_input:
                    admin_email_input.bind(text=self.on_admin_email_change)
                    
                admin_password_input = self.ids.get('admin_password_input')
                if admin_password_input:
                    admin_password_input.bind(text=self.on_admin_password_change)
                    
                admin_password_confirm_input = self.ids.get('admin_password_confirm_input')
                if admin_password_confirm_input:
                    admin_password_confirm_input.bind(text=self.on_admin_password_confirm_change)
                    
            self._bindings_setup = True
            print("Bindings configurados correctamente")
                
        except Exception as e:
            print(f"Error configurando bindings: {e}")

    # Callbacks para actualizar las StringProperties
    def on_company_name_change(self, instance, value):
        self.company_name = value

    def on_company_email_change(self, instance, value):
        self.company_email = value

    def on_company_password_change(self, instance, value):
        self.company_password = value
        self.on_password_change()

    def on_company_password_confirm_change(self, instance, value):
        self.company_password_confirm = value
        self.on_password_change()

    def on_driver_name_change(self, instance, value):
        self.driver_name = value

    def on_driver_email_change(self, instance, value):
        self.driver_email = value

    def on_driver_password_change(self, instance, value):
        self.driver_password = value
        self.on_password_change()

    def on_driver_password_confirm_change(self, instance, value):
        self.driver_password_confirm = value
        self.on_password_change()

    def on_admin_name_change(self, instance, value):
        # No tienes StringProperty para admin_name, así que solo validamos
        self.on_password_change()

    def on_admin_email_change(self, instance, value):
        # No tienes StringProperty para admin_email, así que solo validamos
        self.on_password_change()

    def on_admin_password_change(self, instance, value):
        # No tienes StringProperty para admin_password, así que solo validamos
        self.on_password_change()

    def on_admin_password_confirm_change(self, instance, value):
        self.admin_password_confirm = value
        self.on_password_change()

    def on_password_change(self, *args):
        """Método llamado cuando cambia el texto de las contraseñas."""
        # Usar Clock.schedule_once para evitar llamadas múltiples
        Clock.schedule_once(lambda dt: self.update_password_status(), 0.1)

    def update_password_status(self):
        """Actualiza el indicador de estado de las contraseñas."""
        try:
            password_status_label = self.ids.get('password_status_label')
            if not password_status_label:
                return
            
            # Obtener los campos de contraseña según el tipo de cuenta
            password_field = None
            confirm_field = None
            
            if self.account_type == "company":
                password_field = self.ids.get('company_password_input')
                confirm_field = self.ids.get('company_password_confirm_input')
            elif self.account_type == "driver":
                password_field = self.ids.get('driver_password_input')
                confirm_field = self.ids.get('driver_password_confirm_input')
            elif self.account_type == "admin":
                password_field = self.ids.get('admin_password_input')
                confirm_field = self.ids.get('admin_password_confirm_input')
            
            if not password_field or not confirm_field:
                password_status_label.text = ""
                return
            
            password = password_field.text
            confirm_password = confirm_field.text
            
            # Verificar si ambos campos están vacíos
            if not password and not confirm_password:
                password_status_label.text = ""
                password_status_label.color = self.colors['text_secondary']
                return
            
            # Verificar longitud mínima
            if password and len(password) < 6:
                password_status_label.text = "La contraseña debe tener al menos 6 caracteres"
                password_status_label.color = (1, 0.3, 0.3, 1)  # Rojo
                return
            
            # Verificar si las contraseñas coinciden
            if password and confirm_password:
                if password == confirm_password:
                    if len(password) >= 6:
                        password_status_label.text = "Las contraseñas coinciden"
                        password_status_label.color = (0.2, 0.7, 0.2, 1)  # Verde
                    else:
                        password_status_label.text = "Las contraseñas coinciden pero son muy cortas"
                        password_status_label.color = (1, 0.6, 0, 1)  # Naranja
                else:
                    password_status_label.text = "Las contraseñas no coinciden"
                    password_status_label.color = (1, 0.3, 0.3, 1)  # Rojo
            elif confirm_password:
                password_status_label.text = "Ingresa la contraseña principal primero"
                password_status_label.color = self.colors['text_secondary']
            else:
                password_status_label.text = "Confirma tu contraseña"
                password_status_label.color = self.colors['text_secondary']
                
        except Exception as e:
            print(f"Error actualizando el estado de contraseñas: {e}")

    def clear_fields_for_company(self):
        """Limpiar campos que no son necesarios para Company"""
        try:
            # Usar Clock.schedule_once para asegurar que los widgets estén disponibles
            Clock.schedule_once(self._clear_driver_admin_fields, 0.05)
        except Exception as e:
            print(f"Error limpiando campos: {e}")

    def _clear_driver_admin_fields(self, dt):
        """Limpia los campos de driver y admin."""
        try:
            if hasattr(self, 'ids'):
                driver_fields = ['driver_name_input', 'driver_email_input', 
                               'driver_password_input', 'driver_password_confirm_input']
                admin_fields = ['admin_name_input', 'admin_email_input', 
                              'admin_password_input', 'admin_password_confirm_input']
                
                for field_id in driver_fields + admin_fields:
                    field = self.ids.get(field_id)
                    if field:
                        field.text = ""
        except Exception as e:
            print(f"Error limpiando campos driver/admin: {e}")

    def clear_fields_for_driver(self):
        """Limpiar campos que no son necesarios para Driver"""
        try:
            Clock.schedule_once(self._clear_company_admin_fields, 0.05)
        except Exception as e:
            print(f"Error limpiando campos: {e}")

    def _clear_company_admin_fields(self, dt):
        """Limpia los campos de company y admin."""
        try:
            if hasattr(self, 'ids'):
                company_fields = ['company_name_input', 'company_email_input', 
                                'company_password_input', 'company_password_confirm_input']
                admin_fields = ['admin_name_input', 'admin_email_input', 
                              'admin_password_input', 'admin_password_confirm_input']
                
                for field_id in company_fields + admin_fields:
                    field = self.ids.get(field_id)
                    if field:
                        field.text = ""
        except Exception as e:
            print(f"Error limpiando campos company/admin: {e}")

    # [El resto de métodos permanecen igual - show_error_popup, validate_email, etc.]
    
    def show_error_popup(self, title, message):
        """Muestra un popup con un mensaje de error."""
        content = BoxLayout(
            orientation='vertical', 
            padding=dp(15), 
            spacing=dp(10)
        )
        
        # Crear canvas personalizado para el popup
        with content.canvas.before:
            from kivy.graphics import Color, RoundedRectangle, Line
            Color(*self.colors['background'])
            content.bg_rect = RoundedRectangle(
                size=content.size, 
                pos=content.pos, 
                radius=[dp(12)]
            )
            Color(*self.colors['border'])
            content.border_line = Line(
                width=dp(1),
                rounded_rectangle=(content.x, content.y, content.width, content.height, dp(12))
            )
        
        label = Label(
            text=message,
            text_size=(dp(280), None),
            halign='center',
            valign='middle',
            color=self.colors['text'],
            font_size=dp(14)
        )
        
        button = Button(
            text='Cerrar',
            size_hint=(1, None),
            height=dp(45),
            background_color=(0, 0, 0, 0),
            color=self.colors['text'],
            font_size=dp(14),
            bold=True
        )
        
        # Canvas personalizado para el botón
        with button.canvas.before:
            from kivy.graphics import Color, RoundedRectangle, Line
            Color(*self.colors['primary'])
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
        
        def update_button_canvas(instance, value):
            if hasattr(instance, 'bg_rect'):
                instance.bg_rect.pos = instance.pos
                instance.bg_rect.size = instance.size
            if hasattr(instance, 'border_line'):
                instance.border_line.rounded_rectangle = (
                    instance.x, instance.y, instance.width, instance.height, dp(8)
                )
        
        button.bind(size=update_button_canvas, pos=update_button_canvas)
        
        content.add_widget(label)
        content.add_widget(button)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.85, 0.4),
            auto_dismiss=False,
            background_color=self.colors['surface'],
            title_color=self.colors['text']
        )
        
        def update_content_canvas(instance, value):
            if hasattr(instance, 'bg_rect'):
                instance.bg_rect.pos = instance.pos
                instance.bg_rect.size = instance.size
            if hasattr(instance, 'border_line'):
                instance.border_line.rounded_rectangle = (
                    instance.x, instance.y, instance.width, instance.height, dp(12)
                )
        
        content.bind(size=update_content_canvas, pos=update_content_canvas)
        button.bind(on_press=popup.dismiss)
        popup.open()

    def validate_email(self, email):
        """Valida que el email tenga un formato correcto."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None

    def validate_name(self, name):
        """Valida que el nombre tenga un formato correcto."""
        if not name or len(name.strip()) < 2:
            return False, "El nombre debe tener al menos 2 caracteres."
        
        if len(name.strip()) > 50:
            return False, "El nombre no puede tener más de 50 caracteres."
        
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\-']+$", name.strip()):
            return False, "El nombre solo puede contener letras, espacios, guiones y apostrofes."
        
        return True, ""

    def validate_company_name(self, name):
        """Valida que el nombre de la compañía tenga un formato correcto."""
        if not name or len(name.strip()) < 2:
            return False, "El nombre de la compañía debe tener al menos 2 caracteres."
        
        if len(name.strip()) > 100:
            return False, "El nombre de la compañía no puede tener más de 100 caracteres."
        
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s\-'&.,()]+$", name.strip()):
            return False, "El nombre de la compañía contiene caracteres no válidos."
        
        return True, ""

    def validate_passwords(self, password, password_confirm):
        """Valida que las contraseñas coincidan y cumplan con los requisitos mínimos."""
        if not password or not password_confirm:
            return False, "Ambos campos de contraseña son obligatorios."
        
        if password != password_confirm:
            return False, "Las contraseñas no coinciden."
        
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres."
        
        if len(password) > 128:
            return False, "La contraseña no puede tener más de 128 caracteres."
        
        if not re.search(r'[a-zA-Z]', password):
            return False, "La contraseña debe contener al menos una letra."
        
        if not re.search(r'[0-9]', password):
            return False, "La contraseña debe contener al menos un número."
        
        if ' ' in password:
            return False, "La contraseña no puede contener espacios."
        
        return True, ""

    def sanitize_input(self, text):
        """Sanitiza el input removiendo caracteres peligrosos y espacios extra."""
        if not text:
            return ""
        
        text = text.strip()
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text

    def validate_company_fields(self):
        """Valida todos los campos para el registro de compañía."""
        try:
            name = self.sanitize_input(self.ids.company_name_input.text)
            email = self.sanitize_input(self.ids.company_email_input.text)
            password = self.ids.company_password_input.text
            password_confirm = self.ids.company_password_confirm_input.text

            # Validar nombre de compañía
            is_valid, error_msg = self.validate_company_name(name)
            if not is_valid:
                return False, error_msg

            # Validar email
            if not email:
                return False, "El correo electrónico es obligatorio."
            
            if not self.validate_email(email):
                return False, "El formato del correo electrónico no es válido."

            # Validar contraseñas
            is_valid, error_msg = self.validate_passwords(password, password_confirm)
            if not is_valid:
                return False, error_msg

            return True, ""
        except Exception as e:
            return False, f"Error validando campos: {str(e)}"

    def validate_driver_fields(self):
        """Valida todos los campos para el registro de conductor."""
        try:
            name = self.sanitize_input(self.ids.driver_name_input.text)
            email = self.sanitize_input(self.ids.driver_email_input.text)
            password = self.ids.driver_password_input.text
            password_confirm = self.ids.driver_password_confirm_input.text

            # Validar nombre
            is_valid, error_msg = self.validate_name(name)
            if not is_valid:
                return False, error_msg

            # Validar email
            if not email:
                return False, "El correo electrónico es obligatorio."
            
            if not self.validate_email(email):
                return False, "El formato del correo electrónico no es válido."

            # Validar contraseñas
            is_valid, error_msg = self.validate_passwords(password, password_confirm)
            if not is_valid:
                return False, error_msg

            # Validar que se haya seleccionado una compañía
            if not self.company_id:
                return False, "Debe seleccionar una compañía."

            return True, ""
        except Exception as e:
            return False, f"Error validando campos: {str(e)}"

    def validate_admin_fields(self):
        """Valida todos los campos para el registro de administrador."""
        try:
            name = self.sanitize_input(self.ids.admin_name_input.text)
            email = self.sanitize_input(self.ids.admin_email_input.text)
            password = self.ids.admin_password_input.text
            password_confirm = self.ids.admin_password_confirm_input.text

            # Validar nombre
            is_valid, error_msg = self.validate_name(name)
            if not is_valid:
                return False, error_msg

            # Validar email
            if not email:
                return False, "El correo electrónico es obligatorio."
            
            if not self.validate_email(email):
                return False, "El formato del correo electrónico no es válido."

            # Validar contraseñas
            is_valid, error_msg = self.validate_passwords(password, password_confirm)
            if not is_valid:
                return False, error_msg

            # Validar que se haya seleccionado una compañía
            if not self.company_id:
                return False, "Debe seleccionar una compañía."

            return True, ""
        except Exception as e:
            return False, f"Error validando campos: {str(e)}"

    def go_back(self):
        """Navega hacia la pantalla anterior (Login)."""
        self.manager.current = 'login'

    def register_action(self):
        """Método ejecutado cuando se hace clic en el botón 'Registrar'."""
        print("Botón 'Registrar' presionado.")
        
        try:
            if self.account_type == "company":
                # Validar campos de compañía
                is_valid, error_msg = self.validate_company_fields()
                if not is_valid:
                    self.show_error_popup("Error de Validación", error_msg)
                    return
                
                # Capturar datos sanitizados
                name = self.sanitize_input(self.ids.company_name_input.text)
                email = self.sanitize_input(self.ids.company_email_input.text).lower()
                password = self.ids.company_password_input.text

                # Llamar a la función de registro de la base de datos
                company_data = register_company(name, email, password)
                if company_data:
                    print(f"Compañía '{name}' registrada correctamente.")
                    
                    # Guardar la sesión en current_user
                    App.get_running_app().current_user = {
                        "role": "company",
                        "id": company_data["id"],
                        "name": company_data["name"],
                        "email": company_data["email"]
                    }
                    
                    # Redirigir a la pantalla de dashboard_company
                    self.manager.current = 'dashboard_company'
                else:
                    self.show_error_popup("Error de Registro", "No se pudo registrar la compañía. Posiblemente el email ya existe.")
            
            elif self.account_type == "driver":
                # Validar campos de conductor
                is_valid, error_msg = self.validate_driver_fields()
                if not is_valid:
                    self.show_error_popup("Error de Validación", error_msg)
                    return
                
                # Capturar datos sanitizados
                name = self.sanitize_input(self.ids.driver_name_input.text)
                email = self.sanitize_input(self.ids.driver_email_input.text).lower()
                password = self.ids.driver_password_input.text

                # Llamar a la función de registro de la base de datos para el conductor
                driver_data = register_driver(name, email, password, self.company_id)
                if driver_data:
                    print("Conductor registrado correctamente.")
                    
                    # Guardar la sesión en current_user
                    App.get_running_app().current_user = {
                        "role": "driver",
                        "id": driver_data["id"],
                        "name": driver_data["name"],
                        "email": driver_data["email"],
                        "company_id": driver_data["company_id"]
                    }
                    
                    # Redirigir a la pantalla de init_report
                    self.manager.current = 'init_report'
                else:
                    self.show_error_popup("Error de Registro", "No se pudo registrar el conductor. Posiblemente el email ya existe.")
            
            elif self.account_type == "admin":
                # Validar campos de administrador
                is_valid, error_msg = self.validate_admin_fields()
                if not is_valid:
                    self.show_error_popup("Error de Validación", error_msg)
                    return
                
                # Capturar datos sanitizados
                name = self.sanitize_input(self.ids.admin_name_input.text)
                email = self.sanitize_input(self.ids.admin_email_input.text).lower()
                password = self.ids.admin_password_input.text

                # Llamar a la función de registro de la base de datos para el administrador
                admin_data = register_admin(name, email, password, self.company_id)
                if admin_data:
                    print("Administrador registrado correctamente.")
                    
                    # Guardar la sesión en current_user
                    App.get_running_app().current_user = {
                        "role": "admin",
                        "id": admin_data["id"],
                        "name": admin_data["name"],
                        "email": admin_data["email"],
                        "company_id": admin_data["company_id"]
                    }
                    
                    # Redirigir a la pantalla de dashboard_admin
                    self.manager.current = 'dashboard_admin'
                else:
                    self.show_error_popup("Error de Registro", "No se pudo registrar el administrador. Posiblemente el email ya existe.")
        
        except Exception as e:
            print(f"Ocurrió un error inesperado durante el registro: {e}")
            self.show_error_popup("Error Inesperado", f"Ocurrió un error durante el registro: {str(e)}")
        
    def get_company_list(self):
        """Obtiene una lista de las compañías registradas."""
        try:
            companies = get_all_companies()
            print(f"Compañías obtenidas de la base de datos: {companies}")
            if companies:
                return [company['name'] for company in companies]
            else:
                return ["No hay compañías registradas"]
        except Exception as e:
            print(f"Error al obtener la lista de compañías: {e}")
            return ["Error al cargar compañías"]

    def on_company_selected(self, company_name):
        """Maneja la selección de una compañía desde el Spinner."""
        try:
            # Validar que no sea el mensaje de error o vacío
            if company_name in ["No hay compañías registradas", "Error al cargar compañías", ""]:
                self.company_id = ""
                print("No se seleccionó una compañía válida.")
                return
            
            companies = get_all_companies()
            print(f"Compañías disponibles: {companies}")

            for company in companies:
                if company['name'] == company_name:
                    self.company_id = str(company['id'])
                    print(f"Compañía seleccionada: {company_name} con ID {self.company_id}")
                    break
            else:
                # Si no se encontró la compañía
                self.company_id = ""
                print(f"No se encontró la compañía: {company_name}")
                
        except Exception as e:
            print(f"Error al seleccionar la compañía: {e}")
            self.company_id = ""