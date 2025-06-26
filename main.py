from kivy.app import App
from kivy.lang import Builder

# Importar pantallas
from logic_screens.init_report_logic import ReportScreen
from logic_screens.end_report_logic import EndReportScreen
from core.index import DriverMonitoringScreen

# Importar widgets
from widgets.logic.header import Header
from widgets.logic.footer import Footer

# Importar layout raíz
from root import RootLayout

# Cargar archivos KV de pantallas
Builder.load_file("screens/init_report.kv")
Builder.load_file("screens/monitoring.kv")
Builder.load_file("screens/end_report.kv")  # si existe

# Cargar archivos KV de widgets
Builder.load_file("widgets/visuals/header.kv")
Builder.load_file("widgets/visuals/footer.kv")

class MainApp(App):
    def build(self):
        return RootLayout()

if __name__ == "__main__":
    MainApp().run()
