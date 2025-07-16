from kivy.uix.screenmanager import Screen
from kivy.app import App

class DashboardCompanyScreen(Screen):
    def on_enter(self):
        self.update_welcome_message()

    def update_welcome_message(self):
        try:
            current_user = App.get_running_app().current_user
            if current_user and current_user.get('name'):
                welcome_text = f"Bienvenido, {current_user.get('name')}"
            else:
                welcome_text = "Bienvenido, Compañía"
            if hasattr(self, 'ids') and 'welcome_label' in self.ids:
                self.ids.welcome_label.text = welcome_text
        except Exception as e:
            print(f"Error al actualizar mensaje de bienvenida: {e}")

    def ver_reportes(self):
        self.manager.current = "view_drivers_company"

    def agregar_administrador(self):
        self.manager.current = "register_admin"

    def cerrar_sesion(self):
        try:
            app = App.get_running_app()

            # Limpiar toda la sesión
            app.clear_sessions()
            app.current_user = None

            print("Sesión cerrada correctamente.")
            self.manager.current = "login"
        except Exception as e:
            print(f"Error al cerrar sesión desde dashboard de empresa: {e}")
            self.manager.current = "login"