from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from database import verify_company_login, verify_driver_login, verify_admin_login
import re
import hashlib
import time

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.failed_attempts = 0
        self.last_attempt_time = 0
        self.lockout_duration = 30  # segundos
        self.max_attempts = 5

    def show_error_popup(self, title, message):
        """
        Muestra un popup con un mensaje de error.
        """
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        label = Label(
            text=message,
            text_size=(350, None),
            halign='center',
            valign='middle'
        )
        
        button = Button(
            text='Cerrar',
            size_hint=(1, 0.3),
            height=40
        )
        
        content.add_widget(label)
        content.add_widget(button)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.5),
            auto_dismiss=False
        )
        
        button.bind(on_press=popup.dismiss)
        popup.open()

    def validate_email(self, email):
        """
        Valida que el email tenga un formato correcto.
        """
        if not email:
            return False, "El correo electrónico es obligatorio."
        
        if len(email) > 254:
            return False, "El correo electrónico es demasiado largo."
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "El formato del correo electrónico no es válido."
        
        return True, ""

    def validate_password(self, password):
        """
        Valida que la contraseña tenga un formato básico correcto.
        """
        if not password:
            return False, "La contraseña es obligatoria."
        
        if len(password) < 1:
            return False, "La contraseña no puede estar vacía."
        
        if len(password) > 128:
            return False, "La contraseña es demasiado larga."
        
        return True, ""

    def sanitize_input(self, text):
        """
        Sanitiza el input removiendo caracteres peligrosos y espacios extra.
        """
        if not text:
            return ""
        
        # Remover espacios al inicio y final
        text = text.strip()
        
        # Remover caracteres de control
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        
        # Remover múltiples espacios consecutivos
        text = re.sub(r'\s+', ' ', text)
        
        return text

    def is_account_locked(self):
        """
        Verifica si la cuenta está bloqueada por intentos fallidos.
        """
        current_time = time.time()
        if self.failed_attempts >= self.max_attempts:
            if current_time - self.last_attempt_time < self.lockout_duration:
                remaining_time = int(self.lockout_duration - (current_time - self.last_attempt_time))
                return True, remaining_time
            else:
                # Reset después del tiempo de bloqueo
                self.failed_attempts = 0
                return False, 0
        return False, 0

    def record_failed_attempt(self):
        """
        Registra un intento fallido de login.
        """
        self.failed_attempts += 1
        self.last_attempt_time = time.time()
        print(f"Intento fallido #{self.failed_attempts} registrado.")

    def reset_failed_attempts(self):
        """
        Resetea los intentos fallidos después de un login exitoso.
        """
        self.failed_attempts = 0
        self.last_attempt_time = 0

    def clear_error_message(self):
        """
        Limpia el mensaje de error después de un tiempo.
        """
        if hasattr(self.ids, 'error_label'):
            self.ids.error_label.text = ""

    def set_error_message(self, message):
        """
        Establece un mensaje de error y lo limpia después de un tiempo.
        """
        if hasattr(self.ids, 'error_label'):
            self.ids.error_label.text = message
            # Limpiar el mensaje después de 5 segundos
            Clock.schedule_once(lambda dt: self.clear_error_message(), 5)

    def validate_credentials(self, email, password):
        """
        Valida las credenciales antes de intentar el login.
        """
        # Sanitizar inputs
        email = self.sanitize_input(email).lower()
        password = self.sanitize_input(password)

        # Validar email
        is_valid, error_msg = self.validate_email(email)
        if not is_valid:
            return False, error_msg, None, None

        # Validar contraseña
        is_valid, error_msg = self.validate_password(password)
        if not is_valid:
            return False, error_msg, None, None

        return True, "", email, password

    def attempt_login(self, email, password):
        """
        Intenta hacer login con las credenciales proporcionadas.
        """
        try:
            # Intentar login de compañía
            company = verify_company_login(email, password)
            if company:
                return True, "company", company

            # Intentar login de administrador
            admin = verify_admin_login(email, password)
            if admin:
                return True, "admin", admin

            # Intentar login de conductor
            driver = verify_driver_login(email, password)
            if driver:
                return True, "driver", driver

            # Si ningún login fue exitoso
            return False, None, None

        except Exception as e:
            print(f"Error durante el intento de login: {e}")
            return False, None, None

    def handle_successful_login(self, user_type, user_data):
        """
        Maneja un login exitoso.
        """
        self.reset_failed_attempts()
        self.clear_error_message()
        
        # Configurar sesión según el tipo de usuario
        if user_type == "company":
            App.get_running_app().current_user = {
                "role": "company",
                "id": user_data["id"],
                "name": user_data["name"],
                "email": user_data["email"]
            }
            self.manager.current = "dashboard_company"
            print(f"Inicio de sesión exitoso para la empresa: {user_data['name']}")
            
        elif user_type == "admin":
            App.get_running_app().current_user = {
                "role": "admin",
                "id": user_data["id"],
                "name": user_data["name"],
                "email": user_data["email"],
                "company_id": user_data.get("company_id")
            }
            self.manager.current = "dashboard_admin"
            print(f"Inicio de sesión exitoso para administrador: {user_data['name']}")
            
        elif user_type == "driver":
            App.get_running_app().current_user = {
                "role": "driver",
                "id": user_data["id"],
                "name": user_data["name"],
                "email": user_data["email"],
                "company_id": user_data.get("company_id")
            }
            self.manager.current = "init_report"
            print(f"Inicio de sesión exitoso para el conductor: {user_data['name']}")

    def login(self):
        """
        Método principal de login con validaciones completas.
        """
        try:
            # Verificar si la cuenta está bloqueada
            is_locked, remaining_time = self.is_account_locked()
            if is_locked:
                error_msg = f"Cuenta bloqueada por {remaining_time} segundos debido a múltiples intentos fallidos."
                self.set_error_message(error_msg)
                self.show_error_popup("Cuenta Bloqueada", error_msg)
                return

            # Obtener credenciales de los campos de entrada
            email_input = self.ids.email_input.text if hasattr(self.ids, 'email_input') else ""
            password_input = self.ids.password_input.text if hasattr(self.ids, 'password_input') else ""

            # Validar credenciales
            is_valid, error_msg, email, password = self.validate_credentials(email_input, password_input)
            if not is_valid:
                self.set_error_message(error_msg)
                return

            # Intentar login
            success, user_type, user_data = self.attempt_login(email, password)
            
            if success:
                self.handle_successful_login(user_type, user_data)
            else:
                # Registrar intento fallido
                self.record_failed_attempt()
                
                # Mostrar mensaje de error
                error_msg = "Credenciales incorrectas o usuario no válido."
                remaining_attempts = self.max_attempts - self.failed_attempts
                
                if remaining_attempts > 0:
                    error_msg += f" Te quedan {remaining_attempts} intentos."
                
                self.set_error_message(error_msg)
                
                # Mostrar popup si quedan pocos intentos
                if remaining_attempts <= 2 and remaining_attempts > 0:
                    self.show_error_popup(
                        "Advertencia", 
                        f"Credenciales incorrectas. Te quedan {remaining_attempts} intentos antes de que la cuenta sea bloqueada."
                    )

        except Exception as e:
            print(f"Error inesperado durante el login: {e}")
            error_msg = "Ocurrió un error durante el inicio de sesión. Intenta nuevamente."
            self.set_error_message(error_msg)
            self.show_error_popup("Error", error_msg)

    def on_email_input_focus(self, instance, focus):
        """
        Maneja el evento de focus en el campo de email.
        """
        if not focus:  # Cuando pierde el focus
            email = self.sanitize_input(instance.text)
            if email:
                is_valid, error_msg = self.validate_email(email)
                if not is_valid:
                    self.set_error_message(error_msg)
                else:
                    self.clear_error_message()

    def on_password_input_focus(self, instance, focus):
        """
        Maneja el evento de focus en el campo de contraseña.
        """
        if not focus:  # Cuando pierde el focus
            password = self.sanitize_input(instance.text)
            if password:
                is_valid, error_msg = self.validate_password(password)
                if not is_valid:
                    self.set_error_message(error_msg)

    def clear_fields(self):
        """
        Limpia todos los campos de entrada.
        """
        if hasattr(self.ids, 'email_input'):
            self.ids.email_input.text = ""
        if hasattr(self.ids, 'password_input'):
            self.ids.password_input.text = ""
        self.clear_error_message()

    def on_enter(self):
        """
        Se ejecuta cuando se entra a la pantalla de login.
        """
        # Limpiar campos al entrar
        self.clear_error_message()
        
        # Verificar si hay una sesión activa
        app = App.get_running_app()
        if hasattr(app, 'current_user') and app.current_user:
            print("Sesión activa detectada, redirigiendo...")
            role = app.current_user.get('role')
            if role == 'company':
                self.manager.current = 'dashboard_company'
            elif role == 'admin':
                self.manager.current = 'dashboard_admin'
            elif role == 'driver':
                self.manager.current = 'init_report'