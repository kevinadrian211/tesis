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
from screens_logic.company_screens_logic.register_admin_logic import RegisterAdminScreen
from screens_logic.admin_screens_logic.dashboard_admin_logic import DashboardAdminScreen
from screens_logic.company_screens_logic.view_drivers_company_logic import ViewDriversCompanyScreen

# Importar las pantallas de reportes
from screens_logic.company_screens_logic.view_reports_company_logic import ViewReportsCompanyScreen
from screens_logic.company_screens_logic.view_detailed_reports_company_logic import ViewDetailedReportsCompanyScreen
from screens_logic.admin_screens_logic.view_reports_admin_logic import ViewReportsAdminScreen
from screens_logic.admin_screens_logic.view_detailed_reports_admin_logic import ViewDetailedReportsAdminScreen
from screens_logic.admin_screens_logic.view_trips_admin_logic import ViewTripsAdminScreen
from screens_logic.company_screens_logic.view_trips_company_logic import ViewTripsCompanyScreen

# Cargar archivos KV
Builder.load_file("screens/type_account.kv")
Builder.load_file("screens/register.kv")
Builder.load_file("screens/company_screens/dashboard_company.kv")
Builder.load_file("screens/driver_screens/init_report.kv")
Builder.load_file("screens/driver_screens/monitoring.kv")
Builder.load_file("screens/driver_screens/end_report.kv")
Builder.load_file("screens/login.kv")
Builder.load_file("screens/company_screens/register_admin.kv")
Builder.load_file("screens/admin_screens/dashboard_admin.kv")
Builder.load_file("screens/company_screens/view_drivers_company.kv")

# Cargar los KV de reportes
Builder.load_file("screens/company_screens/view_reports_company.kv")
Builder.load_file("screens/company_screens/view_detailed_reports_company.kv")
Builder.load_file("screens/admin_screens/view_reports_admin.kv")
Builder.load_file("screens/admin_screens/view_detailed_reports_admin.kv")
Builder.load_file("screens/admin_screens/view_trips_admin.kv")
Builder.load_file("screens/company_screens/view_trips_company.kv")

class MainApp(App):
    # Variables para guardar sesión activa
    current_company = None
    current_admin = None
    current_driver = None
    
    # Variable para el conductor seleccionado
    selected_driver = None
    
    # Variables para navegación de reportes detallados
    selected_report_type = None  # 'blink' o 'yawn'
    selected_trip_id = None  # ID del viaje específico
    
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
        sm.add_widget(RegisterAdminScreen(name="register_admin"))
        sm.add_widget(DashboardAdminScreen(name="dashboard_admin"))
        sm.add_widget(ViewDriversCompanyScreen(name="view_drivers_company"))
        
        # Agregar las pantallas de reportes
        sm.add_widget(ViewReportsCompanyScreen(name="view_reports_company"))
        sm.add_widget(ViewDetailedReportsCompanyScreen(name="view_detailed_reports_company"))
        sm.add_widget(ViewReportsAdminScreen(name="view_reports_admin"))
        sm.add_widget(ViewDetailedReportsAdminScreen(name="view_detailed_reports_admin"))
        sm.add_widget(ViewTripsAdminScreen(name="view_trips_admin"))
        sm.add_widget(ViewTripsCompanyScreen(name="view_trips_company"))

        return sm
    
    def on_start(self):
        pass
    
    # Función para limpiar todas las sesiones
    def clear_sessions(self):
        self.current_company = None
        self.current_admin = None
        self.current_driver = None
        self.selected_driver = None
        self.selected_report_type = None
        self.selected_trip_id = None
    
    # Función para limpiar sesión de compañía
    def clear_company_session(self):
        self.current_company = None
    
    # Función para limpiar sesión de administrador
    def clear_admin_session(self):
        self.current_admin = None
    
    # Función para limpiar sesión de conductor
    def clear_driver_session(self):
        self.current_driver = None
    
    # Función para limpiar datos de reportes
    def clear_report_data(self):
        self.selected_report_type = None
        self.selected_trip_id = None

if __name__ == "__main__":
    MainApp().run()