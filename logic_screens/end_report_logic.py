# /Users/kevin/Desktop/tesis/logic_screens/end_report_logic.py
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from core.data_reporting.eye_rub_report.eye_rub_reporting import register_eye_rub_listener
from core.data_reporting.blink_report.total_blink_report import register_blink_listener  # Usamos la función correcta para los reportes de resumen de parpadeos
from core.data_reporting.nods_report.nods_reporting import register_nod_listener
from core.data_reporting.yawns_report.total_yawn_report import register_yawn_listener  # Importar el listener de bostezos

# Cargar la interfaz de usuario (archivo .kv)
Builder.load_file("screens/end_report.kv")

class EndReportScreen(Screen):
    def go_to_home(self):
        """Navegar de vuelta a la pantalla inicial"""
        self.manager.current = "init_report"

    def print_blink_summary_report(self, message: str):
        """
        Este método imprimirá el resumen de los parpadeos en la consola.
        """
        print(f"[EndReportScreen - Blink Summary] {message}")

    def print_eye_rub_summary_report(self, message: str):
        """
        Este método imprimirá el resumen de los frotamientos de ojos en la consola.
        """
        print(f"[EndReportScreen - Eye Rub Summary] {message}")

    def print_nod_summary_report(self, message: str):
        """
        Este método imprimirá el resumen de los cabeceos en la consola.
        """
        print(f"[EndReportScreen - Nod Summary] {message}")

    def print_yawn_summary_report(self, message: str):
        """
        Este método imprimirá el resumen de los bostezos en la consola.
        """
        print(f"[EndReportScreen - Yawn Summary] {message}")  # Imprime el mensaje

# Crear una instancia de EndReportScreen
end_report_screen = EndReportScreen()

# Registrar los listeners para recibir los mensajes de resumen de parpadeo
register_blink_listener(end_report_screen.print_blink_summary_report, report_type="summary")  # Para parpadeos (solo resumen)
register_eye_rub_listener(end_report_screen.print_eye_rub_summary_report, report_type="summary")  # Para frotamientos de ojos
register_nod_listener(end_report_screen.print_nod_summary_report, report_type="summary")  # Para cabeceos (solo resumen)
register_yawn_listener(end_report_screen.print_yawn_summary_report, report_type="summary")  # Para bostezos (solo resumen)
