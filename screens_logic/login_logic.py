# login_logic.py
from kivy.uix.screenmanager import Screen
from kivy.app import App  # <-- Agrega esta importación si no está
from database import verify_company_login, verify_driver_login

class LoginScreen(Screen):
    def login(self):
        # Obtener los valores del input
        email = self.ids.email_input.text.strip()
        password = self.ids.password_input.text.strip()

        # Validación: campos vacíos
        if not email or not password:
            self.ids.error_label.text = "Todos los campos son obligatorios."
            return

        # Intentar login como empresa
        company = verify_company_login(email, password)
        if company:
            print(f"Inicio de sesión exitoso para la empresa: {company['name']}")

            # 🔐 Guardar en la instancia global de la app
            App.get_running_app().current_company = {
                "id": company["id"],
                "name": company["name"],
                "email": company["email"]
            }

            self.ids.error_label.text = ""  # Limpiar mensajes de error previos
            self.manager.current = "dashboard_company"
            return

        # Intentar login como conductor
        driver = verify_driver_login(email, password)
        if driver:
            print(f"Inicio de sesión exitoso para el conductor: {driver['name']}")
            self.ids.error_label.text = ""
            self.manager.current = "init_report"
            return

        # Si ninguno coincide
        self.ids.error_label.text = "Credenciales incorrectas o usuario no válido."
