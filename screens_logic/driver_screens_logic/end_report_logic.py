from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.app import App

# Cargar el archivo .kv correspondiente
Builder.load_file("screens/driver_screens/end_report.kv")

class EndReportScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Diccionario para almacenar datos de reportes
        self.report_data = {
            'blink': None,
            'yawn': None,
            'eye_rub': None,
            'nod': None
        }
        
    def on_enter(self):
        """Se ejecuta cuando se entra a la pantalla"""
        print("[INFO] Entrando a EndReportScreen")
        # NO resetear labels aquí, solo si no hay datos previos
        if not any(self.report_data.values()):
            self.reset_labels()
        else:
            # Re-mostrar datos existentes
            self.refresh_all_reports()
        
    def refresh_all_reports(self):
        """Re-muestra todos los reportes almacenados"""
        if self.report_data['blink']:
            self.show_final_blink_report(self.report_data['blink'])
        if self.report_data['yawn']:
            self.show_final_yawn_report(self.report_data['yawn'])
        if self.report_data['eye_rub']:
            self.show_final_eye_rub_report(self.report_data['eye_rub'])
        if self.report_data['nod']:
            self.show_final_nod_report(self.report_data['nod'])
    
    def reset_labels(self):
        """Resetea todos los labels a su estado inicial"""
        self.ids.final_blink_label.text = "📊 Reporte de parpadeos: Cargando..."
        self.ids.final_yawn_label.text = "🟡 Reporte de bostezos: Cargando..."
        self.ids.final_eye_rub_label.text = "👐 Frotamiento de ojos: Cargando..."
        self.ids.final_nod_label.text = "🤕 Cabeceo: Cargando..."
        
    def go_to_home(self):
        self.manager.current = "init_report"

    def show_final_blink_report(self, data):
        """Actualiza el reporte final de parpadeos"""
        self.report_data['blink'] = data
        print(f"[INFO] Actualizando reporte de parpadeos: {data}")
        
        def update_label(dt):
            try:
                # Verificar que la pantalla esté activa
                if self.manager.current != "end_report":
                    print("[WARNING] Intentando actualizar label pero no estamos en end_report")
                    return
                
                count = data.get("total_count", "N/A")
                normal = data.get("normal_reports", "N/A")
                risk = data.get("risk_reports", "N/A")
                microsleeps = data.get("microsleeps", "N/A")
                level = data.get("risk_level", "")
                comment = data.get("comment", "")
                
                new_text = (
                    f"📊 Reporte final de parpadeos:\n"
                    f"🔵 Normales: {normal} | 🔴 Riesgo: {risk}\n"
                    f"🛌 Microsueños: {microsleeps}\n"
                    f"📈 Total: {count} | Riesgo: {level}\n"
                    f"{comment}"
                )
                
                self.ids.final_blink_label.text = new_text
                print(f"[INFO] Label de parpadeos actualizado exitosamente")
                
            except Exception as e:
                print(f"[ERROR] Error actualizando reporte de parpadeos: {e}")
                if hasattr(self, 'ids') and hasattr(self.ids, 'final_blink_label'):
                    self.ids.final_blink_label.text = "❌ Error cargando reporte de parpadeos"
        
        # Usar un delay muy pequeño para asegurar que la pantalla esté lista
        Clock.schedule_once(update_label, 0.05)

    def show_final_yawn_report(self, data):
        """Actualiza el reporte final de bostezos"""
        self.report_data['yawn'] = data
        print(f"[INFO] Actualizando reporte de bostezos: {data}")
        
        def update_label(dt):
            try:
                # Verificar que la pantalla esté activa
                if self.manager.current != "end_report":
                    print("[WARNING] Intentando actualizar label pero no estamos en end_report")
                    return
                
                normal = data.get("normal_reports", "N/A")
                risk = data.get("risk_reports", "N/A")
                
                new_text = (
                    f"🟡 Reporte final de bostezos:\n"
                    f"🔵 Normales: {normal} | 🔴 Riesgo: {risk}"
                )
                
                self.ids.final_yawn_label.text = new_text
                print(f"[INFO] Label de bostezos actualizado exitosamente")
                
            except Exception as e:
                print(f"[ERROR] Error actualizando reporte de bostezos: {e}")
                if hasattr(self, 'ids') and hasattr(self.ids, 'final_yawn_label'):
                    self.ids.final_yawn_label.text = "❌ Error cargando reporte de bostezos"
        
        Clock.schedule_once(update_label, 0.05)

    def show_final_eye_rub_report(self, message):
        """Actualiza el reporte final de frotamiento de ojos"""
        self.report_data['eye_rub'] = message
        print(f"[INFO] Actualizando reporte de frotamiento de ojos: {message}")
        
        def update_label(dt):
            try:
                # Verificar que la pantalla esté activa
                if self.manager.current != "end_report":
                    print("[WARNING] Intentando actualizar label pero no estamos en end_report")
                    return
                
                new_text = f"👐 Frotamiento de ojos final:\n{message}"
                self.ids.final_eye_rub_label.text = new_text
                print(f"[INFO] Label de frotamiento de ojos actualizado exitosamente")
                
            except Exception as e:
                print(f"[ERROR] Error actualizando reporte de frotamiento de ojos: {e}")
                if hasattr(self, 'ids') and hasattr(self.ids, 'final_eye_rub_label'):
                    self.ids.final_eye_rub_label.text = "❌ Error cargando reporte de frotamiento"
        
        Clock.schedule_once(update_label, 0.05)

    def show_final_nod_report(self, message):
        """Actualiza el reporte final de cabeceo"""
        self.report_data['nod'] = message
        print(f"[INFO] Actualizando reporte de cabeceo: {message}")
        
        def update_label(dt):
            try:
                # Verificar que la pantalla esté activa
                if self.manager.current != "end_report":
                    print("[WARNING] Intentando actualizar label pero no estamos en end_report")
                    return
                
                new_text = f"🤕 Cabeceo final:\n{message}"
                self.ids.final_nod_label.text = new_text
                print(f"[INFO] Label de cabeceo actualizado exitosamente")
                
            except Exception as e:
                print(f"[ERROR] Error actualizando reporte de cabeceo: {e}")
                if hasattr(self, 'ids') and hasattr(self.ids, 'final_nod_label'):
                    self.ids.final_nod_label.text = "❌ Error cargando reporte de cabeceo"
        
        Clock.schedule_once(update_label, 0.05)

# Función para obtener la instancia actual de la pantalla desde el ScreenManager
def get_end_report_screen():
    """Obtiene la instancia actual de EndReportScreen desde el ScreenManager"""
    app = App.get_running_app()
    if app and hasattr(app, 'root'):
        screen_manager = app.root
        if hasattr(screen_manager, 'get_screen'):
            try:
                return screen_manager.get_screen('end_report')
            except:
                print("[WARNING] No se pudo encontrar la pantalla 'end_report'")
                return None
    return None