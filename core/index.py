from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.animation import Animation
from kivy.metrics import dp, sp
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

# === IMPORTAR SISTEMA DE ALARMA ===
from .alert_system.microsleep_alert import (
    dismiss_alarm_safely, 
    dismiss_alarm_with_attention_check,
    verify_attention_and_dismiss,
    is_alarm_playing,
    get_dismiss_button_state,
    format_alarm_duration,
    emergency_stop,
    register_ui_callback,
)

class MicrosleepAlarmPopup(Popup):
    """Popup personalizado para manejar la alarma de microsueño"""
    
    def __init__(self, parent_screen, **kwargs):
        super().__init__(**kwargs)
        self.parent_screen = parent_screen
        self.attention_data = None
        self.update_event = None
        
        # Inicializar colores
        self.colors = {
            'background': (255/255, 252/255, 242/255, 1),  # #FFFCF2
            'surface': (204/255, 197/255, 185/255, 1),     # #CCC5B9
            'primary': (168/255, 159/255, 145/255, 1),     # #A89F91
            'border': (20/255, 26/255, 28/255, 1),         # #141A1C
            'text': (20/255, 26/255, 28/255, 1),           # #141A1C
            'text_secondary': (20/255, 26/255, 28/255, 0.7),
            'alert': (1, 0.2, 0.2, 1),  # Rojo para alertas
            'success': (0.2, 0.8, 0.2, 1),  # Verde para éxito
            'warning': (1, 0.5, 0, 1)  # Naranja para advertencias
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz del popup"""
        self.title = "ALERTA DE MICROSUEÑO"
        self.size_hint = (0.9, 0.7)
        self.auto_dismiss = False  # No se puede cerrar tocando fuera
        
        # Layout principal con canvas personalizado
        main_layout = BoxLayout(
            orientation='vertical', 
            spacing=dp(12), 
            padding=dp(20)
        )
        
        with main_layout.canvas.before:
            Color(*self.colors['background'])
            main_layout.bg_rect = RoundedRectangle(
                size=main_layout.size, 
                pos=main_layout.pos, 
                radius=[dp(12)]
            )
            Color(*self.colors['border'])
            main_layout.border_line = Line(
                width=dp(1),
                rounded_rectangle=(main_layout.x, main_layout.y, main_layout.width, main_layout.height, dp(12))
            )
        
        main_layout.bind(size=self.update_canvas_rect, pos=self.update_canvas_rect)
        
        # Mensaje principal
        self.main_message = self.create_message_widget(
            "¡MICROSUEÑO DETECTADO!\nPor tu seguridad, mantente despierto.",
            sp(18),
            True,
            self.colors['alert']
        )
        main_layout.add_widget(self.main_message)
        
        # Estado de la alarma
        self.status_label = self.create_message_widget(
            "Estado: Iniciando...",
            sp(14),
            False,
            self.colors['text_secondary']
        )
        main_layout.add_widget(self.status_label)
        
        # Área para pregunta de atención
        self.attention_layout = BoxLayout(
            orientation='vertical', 
            spacing=dp(10),
            size_hint_y=None,
            height=dp(80)
        )
        
        self.question_label = self.create_message_widget(
            "",
            sp(16),
            True,
            self.colors['text']
        )
        self.attention_layout.add_widget(self.question_label)
        
        self.answer_input = self.create_text_input()
        self.attention_layout.add_widget(self.answer_input)
        
        main_layout.add_widget(self.attention_layout)
        
        # Botones
        button_layout = BoxLayout(
            orientation='horizontal', 
            spacing=dp(15), 
            size_hint_y=None, 
            height=dp(50)
        )
        
        self.dismiss_button = self.create_custom_button(
            "Desactivar Alarma",
            0.6,
            self.colors['success'],
            self.try_dismiss_alarm
        )
        button_layout.add_widget(self.dismiss_button)
        
        self.emergency_button = self.create_custom_button(
            "EMERGENCIA",
            0.4,
            self.colors['alert'],
            self.emergency_stop
        )
        button_layout.add_widget(self.emergency_button)
        
        main_layout.add_widget(button_layout)
        self.content = main_layout
    
    def create_message_widget(self, text, font_size, bold, color):
        """Crea un widget de mensaje con estilo personalizado"""
        return Label(
            text=text,
            font_size=font_size,
            color=color,
            bold=bold,
            halign='center',
            valign='middle',
            text_size=(None, None)
        )
    
    def create_text_input(self):
        """Crea un TextInput con estilo personalizado"""
        text_input = TextInput(
            hint_text="Escribe tu respuesta aquí",
            font_size=sp(16),
            size_hint_y=None,
            height=dp(40),
            multiline=False,
            background_color=(0, 0, 0, 0)
        )
        
        with text_input.canvas.before:
            Color(*self.colors['surface'])
            text_input.bg_rect = RoundedRectangle(
                size=text_input.size, 
                pos=text_input.pos, 
                radius=[dp(8)]
            )
            Color(*self.colors['border'])
            text_input.border_line = Line(
                width=dp(1),
                rounded_rectangle=(text_input.x, text_input.y, text_input.width, text_input.height, dp(8))
            )
        
        text_input.bind(size=self.update_canvas_rect, pos=self.update_canvas_rect)
        return text_input
    
    def create_custom_button(self, text, size_hint_x, bg_color, callback):
        """Crea un botón con canvas personalizado"""
        button = Button(
            text=text,
            font_size=sp(14),
            bold=True,
            color=self.colors['text'],
            size_hint_x=size_hint_x,
            background_color=(0, 0, 0, 0)
        )
        
        with button.canvas.before:
            Color(*bg_color)
            button.bg_rect = RoundedRectangle(
                size=button.size, 
                pos=button.pos, 
                radius=[dp(8)]
            )
            Color(*self.colors['border'])
            button.border_line = Line(
                width=dp(1),
                rounded_rectangle=(button.x, button.y, button.width, button.height, dp(8))
            )
        
        button.bind(size=self.update_canvas_rect, pos=self.update_canvas_rect)
        button.bind(on_press=callback)
        return button
    
    def update_canvas_rect(self, instance, value):
        """Actualiza los rectángulos del canvas cuando cambia el tamaño"""
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
        if hasattr(instance, 'border_line'):
            instance.border_line.rounded_rectangle = (
                instance.x, instance.y, instance.width, instance.height, dp(8)
            )
        
    def on_open(self):
        """Se ejecuta cuando se abre el popup"""
        print("[POPUP] Popup de alarma abierto")
        self.start_updates()
        
    def on_dismiss(self):
        """Se ejecuta cuando se cierra el popup"""
        print("[POPUP] Popup de alarma cerrado")
        self.stop_updates()
        
    def start_updates(self):
        """Inicia las actualizaciones periódicas del popup"""
        self.update_event = Clock.schedule_interval(self.update_status, 0.5)
        
    def stop_updates(self):
        """Detiene las actualizaciones periódicas"""
        if self.update_event:
            self.update_event.cancel()
            self.update_event = None
            
    def update_status(self, dt):
        """Actualiza el estado del popup periódicamente"""
        if not is_alarm_playing():
            # Si no hay alarma, cerrar popup
            self.dismiss()
            return False
            
        # Actualizar estado del botón
        button_state = get_dismiss_button_state()
        self.dismiss_button.text = button_state["text"]
        self.dismiss_button.disabled = not button_state["enabled"]
        
        # Actualizar duración
        duration_text = format_alarm_duration()
        self.status_label.text = f"Estado: {duration_text}"
        
    def try_dismiss_alarm(self, instance):
        """Intenta desactivar la alarma"""
        print("[POPUP] Intentando desactivar alarma...")
        
        # Intentar desactivación con verificación de atención
        result = dismiss_alarm_with_attention_check()
        
        if result["success"]:
            # Alarma desactivada exitosamente
            self.show_success_message(result["message"])
            Clock.schedule_once(lambda dt: self.dismiss(), 1.5)
            
        elif result.get("requires_attention", False):
            # Se requiere prueba de atención
            self.show_attention_check(result)
            
        else:
            # No se puede desactivar aún
            self.show_error_message(result["message"])
            
    def show_attention_check(self, result):
        """Muestra la pregunta de atención"""
        self.attention_data = result["attention_data"]
        self.question_label.text = f"Para desactivar la alarma, resuelve:\n{self.attention_data['question']} = ?"
        self.answer_input.text = ""
        
        # Cambiar el botón para verificar respuesta
        self.dismiss_button.text = "Verificar Respuesta"
        self.dismiss_button.unbind(on_press=self.try_dismiss_alarm)
        self.dismiss_button.bind(on_press=self.verify_attention)
        
    def verify_attention(self, instance):
        """Verifica la respuesta de atención"""
        try:
            user_answer = int(self.answer_input.text.strip())
            expected_answer = self.attention_data["expected_answer"]
            
            result = verify_attention_and_dismiss(user_answer, expected_answer)
            
            if result["success"]:
                self.show_success_message(result["message"])
                Clock.schedule_once(lambda dt: self.dismiss(), 1.5)
            else:
                self.show_error_message(result["message"])
                # Resetear para nueva pregunta
                Clock.schedule_once(lambda dt: self.reset_to_dismiss_mode(), 2.0)
                
        except ValueError:
            self.show_error_message("Por favor, ingresa un número válido.")
            
    def reset_to_dismiss_mode(self):
        """Resetea el popup al modo de desactivación normal"""
        self.question_label.text = ""
        self.answer_input.text = ""
        self.attention_data = None
        
        # Restaurar botón original
        self.dismiss_button.text = "Desactivar Alarma"
        self.dismiss_button.unbind(on_press=self.verify_attention)
        self.dismiss_button.bind(on_press=self.try_dismiss_alarm)
        
    def show_success_message(self, message):
        """Muestra mensaje de éxito"""
        self.main_message.text = f"✓ {message}"
        self.main_message.color = self.colors['success']
        
    def show_error_message(self, message):
        """Muestra mensaje de error temporalmente"""
        original_text = self.main_message.text
        original_color = self.main_message.color
        
        self.main_message.text = f"✗ {message}"
        self.main_message.color = self.colors['warning']
        
        # Restaurar mensaje original después de 2 segundos
        def restore_message(dt):
            self.main_message.text = original_text
            self.main_message.color = original_color
            
        Clock.schedule_once(restore_message, 2.0)
        
    def emergency_stop(self, instance):
        """Detiene la alarma inmediatamente (emergencia)"""
        print("[POPUP] Parada de emergencia activada")
        emergency_stop()
        self.show_success_message("Alarma detenida por emergencia")
        Clock.schedule_once(lambda dt: self.dismiss(), 1.0)


class DriverMonitoringScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alarm_popup = None
        
        # Inicializar colores según especificaciones
        self.colors = {
            'background': (255/255, 252/255, 242/255, 1),  # #FFFCF2
            'surface': (204/255, 197/255, 185/255, 1),     # #CCC5B9
            'primary': (168/255, 159/255, 145/255, 1),     # #A89F91
            'border': (20/255, 26/255, 28/255, 1),         # #141A1C
            'text': (20/255, 26/255, 28/255, 1),           # #141A1C
            'text_secondary': (20/255, 26/255, 28/255, 0.7)
        }
        
    def on_enter(self):
        """Animación de entrada y configuración inicial"""
        print("[INFO] Entrando a DriverMonitoringScreen: iniciando detectores y cámara.")
        
        # Animación de entrada
        self.load_data()
        self.opacity = 0
        Animation(opacity=1, duration=0.3).start(self)
        
        # === NUEVO: Registrar callback para microsueño ===
        register_ui_callback(self.handle_microsleep_alert)
        
        # Registrar funciones de callback para UI
        gesture_event_receivers.register_callbacks(
            on_eyes=self.update_eyes_report,
            on_blink=self.update_blink_report,
            on_nod=self.update_nod_report,
            on_yawn=self.update_yawn_report,
            on_microsleep=self.handle_microsleep_alert,
        )
        
        self.face_mesh_processor = FaceMeshProcessor()
        self.hand_mesh_processor = HandMeshProcessor()
        self.rotate_frame = True
        
        self.cap = cv2.VideoCapture(1)
        if not self.cap.isOpened():
            self.ids.footer_label.text = "No se pudo abrir la cámara."
            print("[ERROR] No se pudo abrir la cámara.")
            return
        
        print("[INFO] Iniciando hilos de reporte.")
        start_blink_reporting()
        start_yawn_reporting()
        
        self.event = Clock.schedule_interval(self.update, 1.0 / 30.0)

    def load_data(self):
        """Carga datos iniciales (placeholder para consistencia)"""
        pass

    def update(self, dt):
        """Actualiza el frame de video y procesa la detección"""
        ret, frame = self.cap.read()
        if not ret:
            self.ids.footer_label.text = "Error al leer el frame."
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
        
        status_msg = "Detección activa" if face_ok or hand_ok else "Buscando rostro o manos..."
        self.ids.footer_label.text = f"Estado: {status_msg}"

    def on_leave(self):
        """Limpieza al salir de la pantalla"""
        print("[INFO] Saliendo de DriverMonitoringScreen: deteniendo captura y reportes.")
        self.close_alarm_popup()  # Cerrar popup si está abierto
        self.stop_monitoring()
        stop_blink_reporting()
        stop_yawn_reporting()

    def stop_monitoring(self):
        """Detiene el monitoreo de video"""
        if hasattr(self, 'event'):
            self.event.cancel()
            print("[INFO] Evento Clock cancelado.")
        
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
            print("[INFO] Cámara liberada.")

    def end_trip(self):
        """Finaliza el viaje y genera todos los reportes finales"""
        print("[INFO] Iniciando finalización del viaje...")
        
        # Cerrar popup de alarma si está abierto
        self.close_alarm_popup()
        
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
        
        # Programar la generación de reportes después de que la pantalla esté ready
        Clock.schedule_once(generate_reports, 0.8)

    # ===== NUEVO: Manejo de alertas de microsueño =====
    def handle_microsleep_alert(self, message: str):
        """Maneja la alerta de microsueño mostrando el popup"""
        print(f"[MICROSLEEP_ALERT] {message}")
        
        # Actualizar el mensaje en la UI principal
        self.update_microsleep_report(message)
        
        # Mostrar popup de alarma solo si hay una alarma sonando
        if is_alarm_playing() and not self.alarm_popup:
            print("[POPUP] Mostrando popup de alarma de microsueño")
            self.show_alarm_popup()
    
    def show_alarm_popup(self):
        """Muestra el popup de alarma"""
        if self.alarm_popup:
            return  # Ya hay un popup abierto
            
        self.alarm_popup = MicrosleepAlarmPopup(self)
        self.alarm_popup.bind(on_dismiss=self.on_alarm_popup_dismiss)
        self.alarm_popup.open()
    
    def on_alarm_popup_dismiss(self, popup):
        """Se ejecuta cuando se cierra el popup de alarma"""
        print("[POPUP] Popup de alarma cerrado")
        self.alarm_popup = None
    
    def close_alarm_popup(self):
        """Cierra el popup de alarma si está abierto"""
        if self.alarm_popup:
            self.alarm_popup.dismiss()
            self.alarm_popup = None

    # ===== Métodos para actualizar reportes en la UI =====
    def update_eyes_report(self, message: str):
        """Actualiza el reporte de estado de ojos"""
        self.ids.eyes_message_label.text = message

    def update_blink_report(self, message: str):
        """Actualiza el reporte de parpadeo"""
        self.ids.blink_message_label.text = message

    def update_nod_report(self, message: str):
        """Actualiza el reporte de cabeceo"""
        self.ids.nod_message_label.text = message

    def update_yawn_report(self, message: str):
        """Actualiza el reporte de bostezos"""
        self.ids.yawn_message_label.text = message

    def update_microsleep_report(self, message: str):
        """Actualiza el reporte de microsueño"""
        self.ids.microsleep_message_label.text = message

    def create_item_widget(self, data):
        """Crea un widget de elemento con canvas personalizado"""
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(130),
            padding=dp(18),
            spacing=dp(10)
        )
        
        with container.canvas.before:
            Color(*self.colors['background'])
            container.bg_rect = RoundedRectangle(
                size=container.size, 
                pos=container.pos, 
                radius=[dp(12)]
            )
            Color(*self.colors['border'])
            container.border_line = Line(
                width=dp(1),
                rounded_rectangle=(container.x, container.y, container.width, container.height, dp(12))
            )
        
        container.bind(size=self.update_canvas_rect, pos=self.update_canvas_rect)
        return container

    def update_canvas_rect(self, instance, value):
        """Actualiza los rectángulos del canvas cuando cambia el tamaño"""
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
        if hasattr(instance, 'border_line'):
            instance.border_line.rounded_rectangle = (
                instance.x, instance.y, instance.width, instance.height, dp(12)
            )