from kivy.app import App
from kivy.lang import Builder

# Importar pantallas con nuevas rutas
from screens_logic.driver_screens_logic.init_report_logic import ReportScreen
from screens_logic.driver_screens_logic.end_report_logic import EndReportScreen
from core.index import DriverMonitoringScreen  # Esto asumo que sigue siendo correcto

# Cargar archivos KV desde su nueva ubicación
Builder.load_file("screens/driver_screens/init_report.kv")   # ReportScreen
Builder.load_file("screens/driver_screens/monitoring.kv")   # DriverMonitoringScreen
Builder.load_file("screens/driver_screens/end_report.kv")    # EndReportScreen

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
""")

if __name__ == "__main__":
    MainApp().run()
