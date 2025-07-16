from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from database import register_company, register_driver, register_admin, get_all_companies
import re

class RegisterScreen(Screen):
    account_type = StringProperty("")  # Usamos StringProperty para hacer la propiedad reactiva
    company_name = StringProperty("")  # Para el nombre de la compañía
    driver_name = StringProperty("")   # Para el nombre del conductor
    driver_email = StringProperty("")  # Para el correo electrónico del conductor
    driver_password = StringProperty("")  # Para la contraseña del conductor
    company_email = StringProperty("")  # Correo de la compañía
    company_password = StringProperty("")  # Contraseña de la compañía
    company_id = StringProperty("")  # ID de la compañía, solo necesario para conductores

    def on_enter(self):
        """
        Este método se ejecuta cuando se entra en la pantalla de registro.
        Aquí, configuramos los campos a mostrar según el tipo de cuenta.
        """
        print(f"Llegaste como: {self.account_type}")
        
        # Si llegamos como company, se deben mostrar los campos correspondientes a company
        if self.account_type == "company":
            self.clear_fields_for_driver()  # Limpiamos cualquier campo de driver si es una company
            print("Campos de Company visibles.")
        elif self.account_type == "driver":
            self.clear_fields_for_company()  # Limpiamos cualquier campo de company si es un driver
            print("Campos de Driver visibles.")
        
    def clear_fields_for_company(self):
        """Limpiar campos que no son necesarios para Company"""
        self.ids.driver_name_input.text = ""
        self.ids.driver_email_input.text = ""
        self.ids.driver_password_input.text = ""
        self.ids.driver_password_confirm_input.text = ""
        self.ids.company_email_input.text = ""  # Limpiar campo de correo de la compañía
        self.ids.company_password_input.text = ""  # Limpiar campo de contraseña de la compañía
        self.ids.company_password_confirm_input.text = ""

    def clear_fields_for_driver(self):
        """Limpiar campos que no son necesarios para Driver"""
        self.ids.company_name_input.text = ""
        self.ids.company_email_input.text = ""  # Limpiar campo de correo de la compañía
        self.ids.company_password_input.text = ""  # Limpiar campo de contraseña de la compañía
        self.ids.company_password_confirm_input.text = ""

    def show_error_popup(self, title, message):
        """
        Muestra un popup con un mensaje de error.
        """
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        label = Label(
            text=message,
            text_size=(300, None),
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
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )
        
        button.bind(on_press=popup.dismiss)
        popup.open()

    def validate_email(self, email):
        """
        Valida que el email tenga un formato correcto.
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None

    def validate_name(self, name):
        """
        Valida que el nombre tenga un formato correcto.
        """
        if not name or len(name.strip()) < 2:
            return False, "El nombre debe tener al menos 2 caracteres."
        
        if len(name.strip()) > 50:
            return False, "El nombre no puede tener más de 50 caracteres."
        
        # Verificar que no contenga números o caracteres especiales (excepto espacios, guiones y apostrofes)
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\-']+$", name.strip()):
            return False, "El nombre solo puede contener letras, espacios, guiones y apostrofes."
        
        return True, ""

    def validate_company_name(self, name):
        """
        Valida que el nombre de la compañía tenga un formato correcto.
        """
        if not name or len(name.strip()) < 2:
            return False, "El nombre de la compañía debe tener al menos 2 caracteres."
        
        if len(name.strip()) > 100:
            return False, "El nombre de la compañía no puede tener más de 100 caracteres."
        
        # Permitir letras, números, espacios y algunos caracteres especiales comunes en nombres de empresas
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s\-'&.,()]+$", name.strip()):
            return False, "El nombre de la compañía contiene caracteres no válidos."
        
        return True, ""

    def validate_passwords(self, password, password_confirm):
        """
        Valida que las contraseñas coincidan y cumplan con los requisitos mínimos.
        """
        if not password or not password_confirm:
            return False, "Ambos campos de contraseña son obligatorios."
        
        if password != password_confirm:
            return False, "Las contraseñas no coinciden."
        
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres."
        
        if len(password) > 128:
            return False, "La contraseña no puede tener más de 128 caracteres."
        
        # Verificar que contenga al menos una letra y un número
        if not re.search(r'[a-zA-Z]', password):
            return False, "La contraseña debe contener al menos una letra."
        
        if not re.search(r'[0-9]', password):
            return False, "La contraseña debe contener al menos un número."
        
        # Verificar que no contenga espacios
        if ' ' in password:
            return False, "La contraseña no puede contener espacios."
        
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

    def validate_company_fields(self):
        """
        Valida todos los campos para el registro de compañía.
        """
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

    def validate_driver_fields(self):
        """
        Valida todos los campos para el registro de conductor.
        """
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

    def validate_admin_fields(self):
        """
        Valida todos los campos para el registro de administrador.
        """
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

    def go_back(self):
        """
        Esta función maneja la navegación hacia la pantalla anterior (Login).
        Cambia la pantalla activa de ScreenManager a 'login'.
        """
        self.manager.current = 'login'  # Ahora redirige directamente al login

    def register_action(self):
        """
        Este método se ejecuta cuando se hace clic en el botón "Registrar".
        Dependiendo del tipo de cuenta, realiza la validación de los campos.
        """
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
        """
        Obtiene una lista de las compañías registradas.
        Esta función es llamada desde el archivo .kv
        """
        try:
            companies = get_all_companies()  # Obtener todas las compañías de la base de datos
            print(f"Compañías obtenidas de la base de datos: {companies}")
            if companies:
                return [company['name'] for company in companies]  # Retornar solo los nombres
            else:
                return ["No hay compañías registradas"]
        except Exception as e:
            print(f"Error al obtener la lista de compañías: {e}")
            return ["Error al cargar compañías"]

    def on_company_selected(self, company_name):
        """
        Este método maneja la selección de una compañía desde el Spinner.
        Captura el ID de la compañía seleccionada.
        """
        try:
            # Validar que no sea el mensaje de error o vacío
            if company_name in ["No hay compañías registradas", "Error al cargar compañías", ""]:
                self.company_id = ""
                print("No se seleccionó una compañía válida.")
                return
            
            companies = get_all_companies()  # Obtener todas las compañías
            print(f"Compañías disponibles: {companies}")

            for company in companies:
                if company['name'] == company_name:  # Si el nombre coincide
                    self.company_id = str(company['id'])  # Asignar el ID de la compañía como string
                    print(f"Compañía seleccionada: {company_name} con ID {self.company_id}")
                    break
            else:
                # Si no se encontró la compañía
                self.company_id = ""
                print(f"No se encontró la compañía: {company_name}")
                
        except Exception as e:
            print(f"Error al seleccionar la compañía: {e}")
            self.company_id = ""