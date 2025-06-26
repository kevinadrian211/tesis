from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_file("screens/end_report.kv")

class EndReportScreen(Screen):
    def go_to_home(self):
        self.manager.current = "init_report"
