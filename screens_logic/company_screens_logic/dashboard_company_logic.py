from kivy.uix.screenmanager import Screen

class DashboardCompanyScreen(Screen):
    def ver_reportes(self):
        print("Botón 'Ver Reportes' presionado")

    def agregar_administrador(self):
        self.manager.current = "register_admin"
