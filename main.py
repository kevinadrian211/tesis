from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# Importar las pantallas necesarias
from screens_logic.type_account_logic import TypeAccountScreen
from screens_logic.register_logic import RegisterScreen  # Importamos la nueva pantalla de registro
from screens_logic.driver_screens_logic.init_report_logic import ReportScreen
from screens_logic.driver_screens_logic.end_report_logic import EndReportScreen
from core.index import DriverMonitoringScreen
from screens_logic.login_logic import LoginScreen  # Importamos la pantalla de login

# Cargar los archivos KV
Builder.load_file("screens/type_account.kv")  # Pantalla para elegir el tipo de cuenta
Builder.load_file("screens/register.kv")  # Pantalla de registro
Builder.load_file("screens/company_screens/dashboard_company.kv")  # Pantalla del dashboard de la compañía
Builder.load_file("screens/driver_screens/init_report.kv")   # ReportScreen
Builder.load_file("screens/driver_screens/monitoring.kv")   # DriverMonitoringScreen
Builder.load_file("screens/driver_screens/end_report.kv")    # EndReportScreen
Builder.load_file("screens/login.kv")  # Cargamos el archivo KV de la pantalla de login

# Pantalla de la compañía (lo que mostrará después de un registro exitoso)
class DashboardCompanyScreen(Screen):
    pass

# Clase principal de la aplicación
class MainApp(App):
    def build(self):
        sm = ScreenManager()

        # Pantallas
        sm.add_widget(LoginScreen(name="login"))  # Añadimos la pantalla de login como la pantalla inicial
        sm.add_widget(TypeAccountScreen(name="type_account"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(ReportScreen(name="init_report"))
        sm.add_widget(DriverMonitoringScreen(name="monitoring"))
        sm.add_widget(EndReportScreen(name="end_report"))
        sm.add_widget(DashboardCompanyScreen(name="dashboard_company"))  # Pantalla de la compañía

        return sm

    def on_start(self):
        # Aquí podríamos cargar la lógica de verificación de usuario
        pass

if __name__ == "__main__":
    MainApp().run()
