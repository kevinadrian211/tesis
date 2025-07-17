from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import time

# === Procesadores de pose ===
from .pose_extraction.face_landmarks.face_landmark_detector import FaceMeshProcessor
from .pose_extraction.hand_landmarks.hand_landmark_detector import HandMeshProcessor

# === Reportes: solo resumen final ===
from .data_reporting.yawns_report.total_yawn_report import force_show_report_summary as show_yawn_summary
from .data_reporting.nods_report.nods_reporting import force_show_report_summary as show_nods_summary
from .data_reporting.eye_rub_report.eye_rub_reporting import force_show_report_summary as show_eye_rub_summary

# === Reportes: iniciar y detener hilos ===
from .data_reporting.blink_report.blink_reporting import start_blink_reporting, stop_blink_reporting
from .data_reporting.yawns_report.yawns_reporting import start_reporting as start_yawn_reporting, stop_reporting as stop_yawn_reporting

# Importar y registrar callbacks
from .report_receivers import gesture_event_receivers

class DriverMonitoringScreen(Screen):
    def on_enter(self):
        print("[INFO] Entrando a DriverMonitoringScreen: iniciando detectores y cámara.")
        
        # Registrar funciones de callback para UI
        gesture_event_receivers.register_callbacks(
            on_eyes=self.update_eyes_report,
            on_blink=self.update_blink_report,
            on_nod=self.update_nod_report,
            on_yawn=self.update_yawn_report,
            on_microsleep=self.update_microsleep_report,
        )
        
        self.face_mesh_processor = FaceMeshProcessor()
        self.hand_mesh_processor = HandMeshProcessor()
        self.rotate_frame = True
        
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.ids.footer_label.text = "❌ No se pudo abrir la cámara."
            print("[ERROR] No se pudo abrir la cámara.")
            return
        
        print("[INFO] Iniciando hilos de reporte.")
        start_blink_reporting()
        start_yawn_reporting()
        
        self.event = Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        ret, frame = self.cap.read()
        if not ret:
            self.ids.footer_label.text = "❌ Error al leer el frame."
            print("[ERROR] No se pudo leer el frame de la cámara.")
            return
        
        base_frame = frame.copy()
        
        _, face_ok, _ = self.face_mesh_processor.process(base_frame, draw=True)
        _, hand_ok, _ = self.hand_mesh_processor.process(base_frame, draw=True)
        
        if self.rotate_frame:
            base_frame = cv2.flip(base_frame, -1)
        
        rgb_frame = cv2.cvtColor(base_frame, cv2.COLOR_BGR2RGB)
        texture = Texture.create(size=(rgb_frame.shape[1], rgb_frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(rgb_frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
        self.ids.img_widget.texture = texture
        
        status_msg = "✅ Detección activa" if face_ok or hand_ok else "🔍 Buscando rostro o manos..."
        self.ids.footer_label.text = status_msg

    def on_leave(self):
        print("[INFO] Saliendo de DriverMonitoringScreen: deteniendo captura y reportes.")
        self.stop_monitoring()
        stop_blink_reporting()
        stop_yawn_reporting()

    def stop_monitoring(self):
        if hasattr(self, 'event'):
            self.event.cancel()
            print("[INFO] Evento Clock cancelado.")
        
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
            print("[INFO] Cámara liberada.")

    def end_trip(self):
        """Finaliza el viaje y genera todos los reportes finales"""
        print("[INFO] Iniciando finalización del viaje...")
        
        # Detener monitoreo primero
        self.stop_monitoring()
        stop_blink_reporting()
        stop_yawn_reporting()
        
        # Cambiar a la pantalla de reporte final PRIMERO
        print("[INFO] Cambiando a pantalla de reporte final...")
        self.manager.current = "end_report"
        
        # Luego generar reportes con delay para asegurar que la pantalla esté lista
        def generate_reports(dt):
            print("[INFO] Generando reportes finales...")
            
            # Importar dentro de la función para evitar problemas de importación circular
            from .data_reporting.blink_report.total_blink_report import force_show_report_summary as show_blink_summary
            
            try:
                # Generar todos los reportes finales con delays escalonados
                print("[INFO] Generando reporte final de parpadeos...")
                show_blink_summary()
                
                # Programar los otros reportes con delays
                def generate_yawn_report(dt):
                    print("[INFO] Generando reporte final de bostezos...")
                    show_yawn_summary()
                
                def generate_nod_report(dt):
                    print("[INFO] Generando reporte final de cabeceos...")
                    show_nods_summary()
                
                def generate_eye_rub_report(dt):
                    print("[INFO] Generando reporte final de frotamiento de ojos...")
                    show_eye_rub_summary()
                    print("[INFO] Todos los reportes finales generados correctamente.")
                
                Clock.schedule_once(generate_yawn_report, 0.1)
                Clock.schedule_once(generate_nod_report, 0.2)
                Clock.schedule_once(generate_eye_rub_report, 0.3)
                
            except Exception as e:
                print(f"[ERROR] Error al generar reportes finales: {e}")
        
        # Programar la generación de reportes después de que la pantalla esté lista
        Clock.schedule_once(generate_reports, 0.8)

    # ===== Métodos para actualizar reportes en la UI =====
    def update_eyes_report(self, message: str):
        self.ids.eyes_message_label.text = message

    def update_blink_report(self, message: str):
        self.ids.blink_message_label.text = message

    def update_nod_report(self, message: str):
        self.ids.nod_message_label.text = message

    def update_yawn_report(self, message: str):
        self.ids.yawn_message_label.text = message

    def update_microsleep_report(self, message: str):
        self.ids.microsleep_message_label.text = message