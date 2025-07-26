
# end_report.py - Código Python Actualizado
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.app import App
from kivy.animation import Animation

# Cargar el archivo .kv correspondiente
Builder.load_file("screens/driver_screens/end_report.kv")

class EndReportScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Inicialización de colores según especificación
        self.colors = {
            'background': (255/255, 252/255, 242/255, 1),  # #FFFCF2
            'surface': (204/255, 197/255, 185/255, 1),     # #CCC5B9
            'primary': (168/255, 159/255, 145/255, 1),     # #A89F91
            'border': (20/255, 26/255, 28/255, 1),         # #141A1C
            'text': (20/255, 26/255, 28/255, 1),           # #141A1C
            'text_secondary': (20/255, 26/255, 28/255, 0.7)
        }
        
        # Diccionario para almacenar datos de reportes
        self.report_data = {
            'blink': None,
            'yawn': None,
            'eye_rub': None,
            'nod': None
        }
        
    def on_enter(self):
        """Se ejecuta cuando se entra a la pantalla con animación"""
        print("[INFO] Entrando a EndReportScreen")
        
        # Animación de entrada
        self.opacity = 0
        Animation(opacity=1, duration=0.3).start(self)
        
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
        self.ids.final_blink_label.text = "Analizando patrones de parpadeo..."
        self.ids.final_yawn_label.text = "Evaluando nivel de somnolencia..."
        self.ids.final_eye_rub_label.text = "Procesando datos de frotamiento..."
        self.ids.final_nod_label.text = "Analizando movimientos de cabeza..."
        
    def go_to_home(self):
        """Navegar al inicio con animación"""
        # Animación de salida
        anim = Animation(opacity=0, duration=0.2)
        anim.bind(on_complete=lambda *args: setattr(self.manager, 'current', 'init_report'))
        anim.start(self)

    def get_overall_risk_level(self):
        """Calcula el nivel de riesgo general basado en todos los reportes"""
        high_risk_count = 0
        medium_risk_count = 0
        
        # Analizar cada reporte para determinar riesgo
        for report_type, data in self.report_data.items():
            if data is None:
                continue
                
            if report_type == 'blink':
                risk_reports = data.get('risk_reports', 0)
                microsleeps = data.get('microsleeps', 0)
                if risk_reports > 5 or microsleeps > 2:
                    high_risk_count += 1
                elif risk_reports > 2 or microsleeps > 0:
                    medium_risk_count += 1
                    
            elif report_type == 'yawn':
                risk_reports = data.get('risk_reports', 0)
                if risk_reports > 8:
                    high_risk_count += 1
                elif risk_reports > 4:
                    medium_risk_count += 1
                    
            elif report_type == 'eye_rub':
                if "ALTO" in str(data):
                    high_risk_count += 1
                elif "MEDIO" in str(data):
                    medium_risk_count += 1
                    
            elif report_type == 'nod':
                if "ALTO" in str(data):
                    high_risk_count += 1
                elif "MEDIO" in str(data):
                    medium_risk_count += 1
        
        # Determinar nivel general
        if high_risk_count >= 2:
            return "RIESGO ALTO"
        elif high_risk_count >= 1 or medium_risk_count >= 2:
            return "RIESGO MEDIO"
        else:
            return "RIESGO BAJO"

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
                
                count = data.get("total_count", 0)
                normal = data.get("normal_reports", 0)
                risk = data.get("risk_reports", 0)
                microsleeps = data.get("microsleeps", 0)
                
                # Crear mensaje más legible sin emojis
                if count == 0:
                    main_text = "No se registraron datos de parpadeo"
                else:
                    main_text = f"Total de reportes: {count}"
                
                status_text = ""
                if microsleeps > 0:
                    status_text = f"{microsleeps} microsueño(s) detectado(s)"
                elif risk > normal:
                    status_text = "Patrón de parpadeo irregular detectado"
                elif risk > 0:
                    status_text = "Algunos episodios de riesgo detectados"
                else:
                    status_text = "Patrón de parpadeo normal"
                
                new_text = f"{main_text}\n{status_text}"
                
                self.ids.final_blink_label.text = new_text
                print(f"[INFO] Label de parpadeos actualizado exitosamente")
                
            except Exception as e:
                print(f"[ERROR] Error actualizando reporte de parpadeos: {e}")
                if hasattr(self, 'ids') and hasattr(self.ids, 'final_blink_label'):
                    self.ids.final_blink_label.text = "Error cargando reporte de parpadeos"
        
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
                
                normal = data.get("normal_reports", 0)
                risk = data.get("risk_reports", 0)
                total = normal + risk
                
                if total == 0:
                    main_text = "No se detectaron bostezos"
                    status_text = "Nivel de somnolencia normal"
                else:
                    main_text = f"Total de bostezos: {total}"
                    
                    if risk > 8:
                        status_text = "Nivel alto de somnolencia"
                    elif risk > 4:
                        status_text = "Nivel moderado de somnolencia"
                    elif risk > 0:
                        status_text = "Algunos episodios de somnolencia"
                    else:
                        status_text = "Nivel normal de somnolencia"
                
                new_text = f"{main_text}\n{status_text}"
                
                self.ids.final_yawn_label.text = new_text
                print(f"[INFO] Label de bostezos actualizado exitosamente")
                
            except Exception as e:
                print(f"[ERROR] Error actualizando reporte de bostezos: {e}")
                if hasattr(self, 'ids') and hasattr(self.ids, 'final_yawn_label'):
                    self.ids.final_yawn_label.text = "Error cargando reporte de bostezos"
        
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
                
                # El message ya viene formateado desde el dispatcher
                self.ids.final_eye_rub_label.text = message
                print(f"[INFO] Label de frotamiento de ojos actualizado exitosamente")
                
            except Exception as e:
                print(f"[ERROR] Error actualizando reporte de frotamiento de ojos: {e}")
                if hasattr(self, 'ids') and hasattr(self.ids, 'final_eye_rub_label'):
                    self.ids.final_eye_rub_label.text = "Error cargando reporte de frotamiento"
        
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
                
                # El message ya viene formateado desde el dispatcher
                self.ids.final_nod_label.text = message
                print(f"[INFO] Label de cabeceo actualizado exitosamente")
                
            except Exception as e:
                print(f"[ERROR] Error actualizando reporte de cabeceo: {e}")
                if hasattr(self, 'ids') and hasattr(self.ids, 'final_nod_label'):
                    self.ids.final_nod_label.text = "Error cargando reporte de cabeceo"
        
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