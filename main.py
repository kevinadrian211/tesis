from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# Importar las pantallas necesarias
from screens_logic.type_account_logic import TypeAccountScreen
from screens_logic.register_logic import RegisterScreen
from screens_logic.driver_screens_logic.init_report_logic import ReportScreen
from screens_logic.driver_screens_logic.end_report_logic import EndReportScreen
from core.index import DriverMonitoringScreen
from screens_logic.login_logic import LoginScreen
from screens_logic.company_screens_logic.dashboard_company_logic import DashboardCompanyScreen
from screens_logic.company_screens_logic.register_admin_logic import RegisterAdminScreen  # Asegúrate de importar la nueva pantalla

# Cargar los archivos KV
Builder.load_file("screens/type_account.kv")
Builder.load_file("screens/register.kv")
Builder.load_file("screens/company_screens/dashboard_company.kv")
Builder.load_file("screens/driver_screens/init_report.kv")
Builder.load_file("screens/driver_screens/monitoring.kv")
Builder.load_file("screens/driver_screens/end_report.kv")
Builder.load_file("screens/login.kv")
Builder.load_file("screens/company_screens/register_admin.kv")  # Cargar el archivo de la pantalla RegisterAdmin

# NOTA: Ya tienes la clase DashboardCompanyScreen importada,
# así que NO la vuelvas a definir aquí para evitar conflicto.

class MainApp(App):
    current_company = None  # 👈 Esta línea habilita el almacenamiento de sesión de empresa
    def build(self):
        sm = ScreenManager()

        # Agregar las pantallas al ScreenManager
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(TypeAccountScreen(name="type_account"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(ReportScreen(name="init_report"))
        sm.add_widget(DriverMonitoringScreen(name="monitoring"))
        sm.add_widget(EndReportScreen(name="end_report"))
        sm.add_widget(DashboardCompanyScreen(name="dashboard_company"))
        sm.add_widget(RegisterAdminScreen(name="register_admin"))  # Pantalla de registro de administrador

        return sm

    def on_start(self):
        pass

if __name__ == "__main__":
    MainApp().run()
