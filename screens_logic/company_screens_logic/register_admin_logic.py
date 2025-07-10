from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.app import App
from database import register_admin  # Asegúrate de que esta función esté importada correctamente

class RegisterAdminScreen(Screen):

    def register_admin(self):
        name = self.ids.admin_name.text.strip()
        email = self.ids.admin_email.text.strip()
        password = self.ids.admin_password.text.strip()
        confirm_password = self.ids.admin_confirm_password.text.strip()

        # Validaciones de campos vacíos
        if not name or not email or not password or not confirm_password:
            self.show_popup("Error", "Todos los campos son obligatorios.")
            return

        # Verificar que las contraseñas coincidan
        if password != confirm_password:
            self.show_popup("Error", "Las contraseñas no coinciden.")
            return

        # Obtener el ID de la compañía desde el App (debe haber sido guardado luego del login)
        app = App.get_running_app()
        company = getattr(app, 'current_company', None)

        if not company:
            self.show_popup("Error", "No se ha identificado a la compañía.")
            return

        company_id = company.get("id")

        # Registrar el administrador en Supabase
        success = register_admin(name, email, password, company_id)

        if success:
            self.clear_fields()
            # Cambiar a la pantalla dashboard_company sin mostrar popup
            self.manager.current = "dashboard_company"
        else:
            self.show_popup("Error", "No se pudo registrar el administrador. Verifica que el email no esté en uso.")

    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.8, 0.4))
        popup.open()

    def clear_fields(self):
        self.ids.admin_name.text = ""
        self.ids.admin_email.text = ""
        self.ids.admin_password.text = ""
        self.ids.admin_confirm_password.text = ""
