from kivy.uix.screenmanager import Screen

class DashboardCompanyScreen(Screen):
    def ver_reportes(self):
        self.manager.current = "view_drivers_company"
        
    def agregar_administrador(self):
        self.manager.current = "register_admin"
