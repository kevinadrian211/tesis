from kivy.uix.screenmanager import Screen
from kivy.lang import Builder


class ReportScreen(Screen):
    def on_start_trip(self):
        self.manager.current = "monitoring"
