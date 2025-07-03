from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# Cargar el archivo KV correspondiente
Builder.load_file("screens/driver_screens/init_report.kv")


class ReportScreen(Screen):
    def on_start_trip(self):
        self.manager.current = "monitoring"
