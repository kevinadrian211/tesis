from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from logic_screens.init_report_logic import ReportScreen
from logic_screens.report_logic import ReportResultScreen

# Cargar KV
Builder.load_file("screens/init_report.kv")
Builder.load_file("screens/report.kv")

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ReportScreen(name="init_report"))
        sm.add_widget(ReportResultScreen(name="report"))
        return sm

if __name__ == "__main__":
    MainApp().run()
