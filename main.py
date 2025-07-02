from kivy.app import App
from kivy.lang import Builder

# Importar pantallas
from logic_screens.init_report_logic import ReportScreen
from logic_screens.end_report_logic import EndReportScreen
from core.index import DriverMonitoringScreen

# Cargar archivos KV de pantallas
Builder.load_file("screens/init_report.kv")  # ReportScreen
Builder.load_file("screens/monitoring.kv")   # DriverMonitoringScreen
Builder.load_file("screens/end_report.kv")   # EndReportScreen

class MainApp(App):
    def build(self):
        return Builder.load_string("""
ScreenManager:
    ReportScreen:
        name: "init_report"
    DriverMonitoringScreen:
        name: "monitoring"
    EndReportScreen:
        name: "end_report"
""")  # Definimos el ScreenManager aquí directamente, pero ya cargamos los archivos .kv

if __name__ == "__main__":
    MainApp().run()
