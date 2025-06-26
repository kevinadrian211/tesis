# main.py
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

# Pantallas de lógica
from logic_screens.init_report_logic import ReportScreen
from core.index import DriverMonitoringScreen
from logic_screens.end_report_logic import EndReportScreen

# Carga de archivos KV
Builder.load_file("screens/init_report.kv")
Builder.load_file("screens/monitoring.kv")

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ReportScreen(name="init_report"))
        sm.add_widget(DriverMonitoringScreen(name="monitoring"))
        sm.add_widget(EndReportScreen(name="end_report"))
        return sm

if __name__ == "__main__":
    MainApp().run()
