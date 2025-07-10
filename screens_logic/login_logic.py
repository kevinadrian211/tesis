from kivy.uix.screenmanager import Screen
from kivy.app import App
from database import verify_company_login, verify_driver_login, verify_admin_login

class LoginScreen(Screen):
    def login(self):
        email = self.ids.email_input.text.strip()
        password = self.ids.password_input.text.strip()

        if not email or not password:
            self.ids.error_label.text = "Todos los campos son obligatorios."
            return

        # Login de compañía
        company = verify_company_login(email, password)
        if company:
            print(f"Inicio de sesión exitoso para la empresa: {company['name']}")
            self.ids.error_label.text = ""

            # Guardar sesión en current_user con rol
            App.get_running_app().current_user = {
                "role": "company",
                "id": company["id"],
                "name": company["name"],
                "email": company["email"]
            }

            self.manager.current = "dashboard_company"
            return

        # Login de administrador
        admin = verify_admin_login(email, password)
        if admin:
            print(f"Inicio de sesión exitoso para administrador: {admin['name']}")
            self.ids.error_label.text = ""

            # Guardar sesión en current_user con rol
            App.get_running_app().current_user = {
                "role": "admin",
                "id": admin["id"],
                "name": admin["name"],
                "email": admin["email"],
                "company_id": admin.get("company_id")
            }

            self.manager.current = "dashboard_admin"
            return

        # Login de conductor
        driver = verify_driver_login(email, password)
        if driver:
            print(f"Inicio de sesión exitoso para el conductor: {driver['name']}")
            self.ids.error_label.text = ""

            # Guardar sesión en current_user con rol
            App.get_running_app().current_user = {
                "role": "driver",
                "id": driver["id"],
                "name": driver["name"],
                "email": driver["email"],
                "company_id": driver.get("company_id")
            }

            self.manager.current = "init_report"
            return

        # Si ningún login fue exitoso
        self.ids.error_label.text = "Credenciales incorrectas o usuario no válido."
