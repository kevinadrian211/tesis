from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# Cargar visuales de widgets
Builder.load_file('widgets/visuals/header.kv')
Builder.load_file('widgets/visuals/footer.kv')

from widgets.logic.header import Header
from widgets.logic.footer import Footer

class ReportScreen(Screen):
    def on_start_trip(self):
        # Cambia a la pantalla "report"
        self.manager.current = "report"
