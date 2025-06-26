from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2

from .pose_extraction.face_landmarks.face_landmark_detector import FaceMeshProcessor
from .pose_extraction.hand_landmarks.hand_landmark_detector import HandMeshProcessor

from core.data_reporting.blink_report.total_blink_report import force_show_report_summary as show_blink_summary
from core.data_reporting.yawns_report.total_yawn_report import force_show_report_summary as show_yawn_summary
from core.data_reporting.nods_report.nods_reporting import force_show_report_summary as show_nods_summary
from core.data_reporting.eye_rub_report.eye_rub_reporting import force_show_report_summary as show_eye_rub_summary

class DriverMonitoringScreen(Screen):
    def on_enter(self):
        self.face_mesh_processor = FaceMeshProcessor()
        self.hand_mesh_processor = HandMeshProcessor()
        self.rotate_frame = True
        self.cap = cv2.VideoCapture(1)

        if not self.cap.isOpened():
            self.ids.footer_label.text = "❌ No se pudo abrir la cámara."
            return

        self.event = Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        ret, frame = self.cap.read()
        if not ret:
            self.ids.footer_label.text = "❌ Error al leer el frame."
            return

        _, face_success, face_frame = self.face_mesh_processor.process(frame.copy(), draw=True)
        _, hand_success, hand_frame = self.hand_mesh_processor.process(frame.copy(), draw=True)

        if face_frame.shape == frame.shape and hand_frame.shape == frame.shape:
            frame_with_both = frame.copy()
            frame_with_both = cv2.addWeighted(frame_with_both, 1.0, face_frame, 1.0, 0)
            frame_with_both = cv2.addWeighted(frame_with_both, 1.0, hand_frame, 1.0, 0)
        else:
            self.ids.footer_label.text = "❌ Tamaño inconsistente en las mallas."
            return

        if self.rotate_frame:
            frame_with_both = cv2.flip(frame_with_both, -1)

        rgb_frame = cv2.cvtColor(frame_with_both, cv2.COLOR_BGR2RGB)
        buf = rgb_frame.tobytes()

        texture = Texture.create(size=(rgb_frame.shape[1], rgb_frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.ids.img_widget.texture = texture

        self.ids.footer_label.text = (
            "✅ Detección activa" if face_success or hand_success else "🔍 Buscando rostro o manos..."
        )

    def on_leave(self):
        self.stop_monitoring()

    def stop_monitoring(self):
        if hasattr(self, 'event'):
            self.event.cancel()
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()

    def end_trip(self):
        self.stop_monitoring()

        # Mostrar los resúmenes manualmente
        show_blink_summary()
        show_yawn_summary()
        show_nods_summary()
        show_eye_rub_summary()

        # Cambiar a la pantalla de resumen final
        self.manager.current = "end_report"
