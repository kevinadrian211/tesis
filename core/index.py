from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2

from pose_extraction.face_landmarks.face_landmark_detector import FaceMeshProcessor
from pose_extraction.hand_landmarks.hand_landmark_detector import HandMeshProcessor


class DriverMonitoringApp(App):
    def build(self):
        # Procesadores de malla
        self.face_mesh_processor = FaceMeshProcessor()
        self.hand_mesh_processor = HandMeshProcessor()

        # Rotar siempre activado desde el inicio
        self.rotate_frame = True

        # Captura de cámara (usa cámara secundaria)
        self.cap = cv2.VideoCapture(1)
        if not self.cap.isOpened():
            print("❌ No se pudo abrir la cámara.")
            return Label(text="❌ No se pudo abrir la cámara.")

        # Layout principal
        root_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Header
        header = Label(text="🧠 Monitor de Atención del Conductor", size_hint=(1, 0.1), font_size='20sp')
        root_layout.add_widget(header)

        # Imagen (video)
        self.img_widget = Image(size_hint=(1, 0.8))
        root_layout.add_widget(self.img_widget)

        # Footer
        self.footer = Label(text="Estado: Iniciando...", size_hint=(1, 0.1), font_size='16sp')
        root_layout.add_widget(self.footer)

        # Actualización del video
        Clock.schedule_interval(self.update, 1.0 / 30.0)

        return root_layout

    def update(self, dt):
        ret, frame = self.cap.read()
        if not ret:
            self.footer.text = "❌ Error al leer el frame."
            return

        # Procesamos sin invertir aún
        _, face_success, face_frame = self.face_mesh_processor.process(frame.copy(), draw=True)
        _, hand_success, hand_frame = self.hand_mesh_processor.process(frame.copy(), draw=True)

        # Combinar resultados
        frame_with_both = frame.copy()
        frame_with_both = cv2.addWeighted(frame_with_both, 1.0, face_frame, 1.0, 0)
        frame_with_both = cv2.addWeighted(frame_with_both, 1.0, hand_frame, 1.0, 0)

        # Rotar siempre la imagen 180 grados (flip -1)
        if self.rotate_frame:
            frame_with_both = cv2.flip(frame_with_both, -1)

        # Convertir BGR → RGB para Kivy
        rgb_frame = cv2.cvtColor(frame_with_both, cv2.COLOR_BGR2RGB)
        buf = rgb_frame.tobytes()

        texture = Texture.create(size=(rgb_frame.shape[1], rgb_frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.img_widget.texture = texture

        # Actualizar footer
        if face_success or hand_success:
            self.footer.text = "✅ Detección activa"
        else:
            self.footer.text = "🔍 Buscando rostro o manos..."

    def on_stop(self):
        self.cap.release()


if __name__ == '__main__':
    DriverMonitoringApp().run()
