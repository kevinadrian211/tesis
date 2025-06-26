from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from widgets.logic.header import Header
from widgets.logic.footer import Footer

class ReportScreen(Screen):
    def on_start_trip(self):
        self.manager.current = "monitoring"
