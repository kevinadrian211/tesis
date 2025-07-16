from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from database import (
    get_minute_reports_by_trip,
    get_5min_reports_by_trip,
    get_10min_reports_by_trip,
    get_eye_rub_reports_by_trip,
    get_nod_reports_by_trip,
    get_all_minute_reports_by_trip
)

class ViewDetailedReportsCompanyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_trip_id = None
        self.current_report_type = None
        self.reports_data = []
        self.current_driver = None
        
    def on_enter(self):
        """
        Se ejecuta al entrar en la pantalla
        """
        self.load_screen_data()
        
    def load_screen_data(self):
        """
        Carga los datos necesarios para la pantalla
        """
        try:
            app = App.get_running_app()
            self.current_report_type = getattr(app, 'selected_report_type', None)
            self.current_trip_id = getattr(app, 'selected_trip_id', None)
            self.current_driver = getattr(app, 'selected_driver', None)
            
            print(f"Cargando reportes detallados - Tipo: {self.current_report_type}, Trip ID: {self.current_trip_id}")
            
            # Actualizar información de la pantalla
            self.update_screen_info()
            
            # Cargar reportes específicos
            self.load_detailed_reports()
            
        except Exception as e:
            print(f"Error al cargar datos de la pantalla: {e}")
            import traceback
            traceback.print_exc()
    
    def update_screen_info(self):
        """
        Actualiza la información general de la pantalla
        """
        try:
            # Actualizar título según el tipo de reporte
            title_text = "Reportes Detallados"
            if self.current_report_type == 'blink':
                title_text = "Reportes Detallados - Parpadeos"
            elif self.current_report_type == 'yawn':
                title_text = "Reportes Detallados - Bostezos"
            elif self.current_report_type == 'eye_rub':
                title_text = "Reportes Detallados - Frotamiento de Ojos"
            elif self.current_report_type == 'nod':
                title_text = "Reportes Detallados - Cabeceo"
            
            self.ids.title_label.text = title_text
            
            # Mostrar información del viaje o conductor
            if self.current_trip_id:
                self.ids.trip_info_label.text = f"Viaje ID: {self.current_trip_id[:8]}..."
            elif self.current_driver:
                driver_name = self.current_driver.get('name', 'N/A')
                self.ids.trip_info_label.text = f"Conductor: {driver_name} - Vista General"
            else:
                self.ids.trip_info_label.text = "Vista general de reportes"
                
        except Exception as e:
            print(f"Error al actualizar información de pantalla: {e}")
    
    def load_detailed_reports(self):
        """
        Carga los reportes detallados según el tipo seleccionado
        """
        try:
            # Si no hay trip_id, intentar obtener todos los reportes del conductor
            if not self.current_trip_id:
                self.load_all_reports_for_driver()
                return
            
            # Cargar reportes según el tipo para un viaje específico
            if self.current_report_type == 'blink':
                self.reports_data = get_minute_reports_by_trip(self.current_trip_id)
                self.display_blink_reports()
            elif self.current_report_type == 'yawn':
                # Cargar reportes de 5 y 10 minutos
                reports_5min = get_5min_reports_by_trip(self.current_trip_id)
                reports_10min = get_10min_reports_by_trip(self.current_trip_id)
                self.display_yawn_reports(reports_5min, reports_10min)
            elif self.current_report_type == 'eye_rub':
                self.reports_data = get_eye_rub_reports_by_trip(self.current_trip_id)
                self.display_eye_rub_reports()
            elif self.current_report_type == 'nod':
                self.reports_data = get_nod_reports_by_trip(self.current_trip_id)
                self.display_nod_reports()
            else:
                print(f"Tipo de reporte no reconocido: {self.current_report_type}")
                self.display_no_data_message()
                
        except Exception as e:
            print(f"Error al cargar reportes detallados: {e}")
            import traceback
            traceback.print_exc()
            self.display_error_message()
    
    def load_all_reports_for_driver(self):
        """
        Carga todos los reportes del conductor para el tipo seleccionado
        """
        try:
            if not self.current_driver:
                print("Error: No hay conductor seleccionado")
                self.display_no_data_message()
                return
            
            # Obtener todos los viajes del conductor desde la app
            app = App.get_running_app()
            selected_trip_id = getattr(app, 'selected_trip_id_for_driver', None)
            
            if not selected_trip_id:
                print("Error: No hay viaje seleccionado para el conductor")
                self.display_no_data_message()
                return
            
            # Cargar reportes para el viaje seleccionado
            if self.current_report_type == 'blink':
                self.reports_data = get_minute_reports_by_trip(selected_trip_id)
                self.display_blink_reports()
            elif self.current_report_type == 'yawn':
                reports_5min = get_5min_reports_by_trip(selected_trip_id)
                reports_10min = get_10min_reports_by_trip(selected_trip_id)
                self.display_yawn_reports(reports_5min, reports_10min)
            elif self.current_report_type == 'eye_rub':
                self.reports_data = get_eye_rub_reports_by_trip(selected_trip_id)
                self.display_eye_rub_reports()
            elif self.current_report_type == 'nod':
                self.reports_data = get_nod_reports_by_trip(selected_trip_id)
                self.display_nod_reports()
            else:
                print(f"Tipo de reporte no reconocido: {self.current_report_type}")
                self.display_no_data_message()
                
        except Exception as e:
            print(f"Error al cargar reportes para el conductor: {e}")
            import traceback
            traceback.print_exc()
            self.display_error_message()
    
    def display_blink_reports(self):
        """
        Muestra los reportes de parpadeo por minuto
        """
        try:
            # Limpiar contenedor
            reports_container = self.ids.reports_container
            reports_container.clear_widgets()
            
            if not self.reports_data:
                self.display_no_data_message()
                return
            
            # Crear encabezado
            header_widget = self.create_blink_header()
            reports_container.add_widget(header_widget)
            
            # Crear widgets para cada reporte
            for i, report in enumerate(self.reports_data):
                report_widget = self.create_blink_report_widget(report, i + 1)
                reports_container.add_widget(report_widget)
                
        except Exception as e:
            print(f"Error al mostrar reportes de parpadeo: {e}")
            self.display_error_message()
    
    def create_blink_header(self):
        """
        Crea el encabezado para los reportes de parpadeo
        """
        header_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            padding=dp(10),
            spacing=dp(10)
        )
        
        # Crear fondo
        with header_container.canvas.before:
            Color(0.2, 0.6, 0.9, 1)
            header_container.rect = Rectangle(size=header_container.size, pos=header_container.pos)
        
        header_container.bind(size=self.update_rect, pos=self.update_rect)
        
        # Crear labels de encabezado
        headers = ["#", "Timestamp", "Parpadeos", "Duración Promedio", "Estado"]
        widths = [0.1, 0.3, 0.2, 0.2, 0.2]
        
        for header, width in zip(headers, widths):
            label = Label(
                text=header,
                font_size=14,
                bold=True,
                size_hint_x=width,
                color=(1, 1, 1, 1),
                halign='center',
                valign='middle'
            )
            header_container.add_widget(label)
        
        return header_container
    
    def create_blink_report_widget(self, report, index):
        """
        Crea un widget para un reporte de parpadeo individual
        """
        container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(35),
            padding=dp(10),
            spacing=dp(10)
        )
        
        # Alternar color de fondo
        bg_color = (0.98, 0.98, 0.98, 1) if index % 2 == 0 else (0.95, 0.95, 0.95, 1)
        
        with container.canvas.before:
            Color(*bg_color)
            container.rect = Rectangle(size=container.size, pos=container.pos)
        
        container.bind(size=self.update_rect, pos=self.update_rect)
        
        # Datos del reporte
        timestamp = report.get('timestamp', 'N/A')
        blink_count = report.get('blink_count', 0)
        avg_duration = report.get('blink_avg_duration', 0)
        
        # Determinar estado basado en los valores
        if blink_count > 20:  # Ejemplo de umbral
            status = "Normal"
            status_color = (0, 0.8, 0, 1)
        elif blink_count < 10:
            status = "Atención"
            status_color = (1, 0.5, 0, 1)
        else:
            status = "Riesgo"
            status_color = (1, 0, 0, 1)
        
        # Crear labels
        data = [
            (str(index), 0.1, (0, 0, 0, 1)),
            (timestamp.split('T')[1][:8] if 'T' in timestamp else timestamp, 0.3, (0, 0, 0, 1)),
            (str(blink_count), 0.2, (0, 0, 0, 1)),
            (f"{avg_duration:.2f}s", 0.2, (0, 0, 0, 1)),
            (status, 0.2, status_color)
        ]
        
        for text, width, color in data:
            label = Label(
                text=text,
                font_size=12,
                size_hint_x=width,
                color=color,
                halign='center',
                valign='middle'
            )
            container.add_widget(label)
        
        return container
    
    def display_yawn_reports(self, reports_5min, reports_10min):
        """
        Muestra los reportes de bostezos (5 y 10 minutos)
        """
        try:
            reports_container = self.ids.reports_container
            reports_container.clear_widgets()
            
            # Título para reportes de 5 minutos
            if reports_5min:
                title_5min = Label(
                    text="Reportes de 5 Minutos",
                    font_size=16,
                    bold=True,
                    size_hint_y=None,
                    height=dp(30),
                    color=(0.2, 0.2, 0.2, 1)
                )
                reports_container.add_widget(title_5min)
                
                for i, report in enumerate(reports_5min):
                    report_widget = self.create_yawn_report_widget(report, i + 1)
                    reports_container.add_widget(report_widget)
            
            # Título para reportes de 10 minutos
            if reports_10min:
                title_10min = Label(
                    text="Reportes de 10 Minutos",
                    font_size=16,
                    bold=True,
                    size_hint_y=None,
                    height=dp(30),
                    color=(0.2, 0.2, 0.2, 1)
                )
                reports_container.add_widget(title_10min)
                
                for i, report in enumerate(reports_10min):
                    report_widget = self.create_yawn_report_widget(report, i + 1)
                    reports_container.add_widget(report_widget)
            
            if not reports_5min and not reports_10min:
                self.display_no_data_message()
                
        except Exception as e:
            print(f"Error al mostrar reportes de bostezos: {e}")
            self.display_error_message()
    
    def create_yawn_report_widget(self, report, index):
        """
        Crea un widget para un reporte de bostezo
        """
        container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(35),
            padding=dp(10),
            spacing=dp(10)
        )
        
        # Alternar color de fondo
        bg_color = (0.98, 0.98, 0.98, 1) if index % 2 == 0 else (0.95, 0.95, 0.95, 1)
        
        with container.canvas.before:
            Color(*bg_color)
            container.rect = Rectangle(size=container.size, pos=container.pos)
        
        container.bind(size=self.update_rect, pos=self.update_rect)
        
        # Datos del reporte
        timestamp = report.get('timestamp', 'N/A')
        yawn_count = report.get('yawn_count', 0)
        avg_duration = report.get('yawn_avg_duration', 0)
        
        # Crear labels
        data = [
            (str(index), 0.15),
            (timestamp.split('T')[1][:8] if 'T' in timestamp else timestamp, 0.3),
            (str(yawn_count), 0.2),
            (f"{avg_duration:.2f}s", 0.2),
            ("Normal" if yawn_count < 5 else "Atención", 0.15)
        ]
        
        for text, width in data:
            label = Label(
                text=text,
                font_size=12,
                size_hint_x=width,
                color=(0, 0, 0, 1),
                halign='center',
                valign='middle'
            )
            container.add_widget(label)
        
        return container
    
    def display_eye_rub_reports(self):
        """
        Muestra los reportes de frotamiento de ojos
        """
        try:
            reports_container = self.ids.reports_container
            reports_container.clear_widgets()
            
            if not self.reports_data:
                self.display_no_data_message()
                return
            
            # Crear encabezado simple
            header_label = Label(
                text="Reportes de Frotamiento de Ojos",
                font_size=16,
                bold=True,
                size_hint_y=None,
                height=dp(30),
                color=(0.2, 0.2, 0.2, 1)
            )
            reports_container.add_widget(header_label)
            
            # Mostrar reportes
            for i, report in enumerate(self.reports_data):
                report_widget = self.create_eye_rub_report_widget(report, i + 1)
                reports_container.add_widget(report_widget)
                
        except Exception as e:
            print(f"Error al mostrar reportes de frotamiento de ojos: {e}")
            self.display_error_message()
    
    def create_eye_rub_report_widget(self, report, index):
        """
        Crea un widget para un reporte de frotamiento de ojos
        """
        container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(35),
            padding=dp(10),
            spacing=dp(10)
        )
        
        # Alternar color de fondo
        bg_color = (0.98, 0.98, 0.98, 1) if index % 2 == 0 else (0.95, 0.95, 0.95, 1)
        
        with container.canvas.before:
            Color(*bg_color)
            container.rect = Rectangle(size=container.size, pos=container.pos)
        
        container.bind(size=self.update_rect, pos=self.update_rect)
        
        # Datos del reporte
        timestamp = report.get('timestamp', 'N/A')
        gesture_count = report.get('gesture_count', 0)
        
        # Crear labels
        data = [
            (str(index), 0.15),
            (timestamp.split('T')[1][:8] if 'T' in timestamp else timestamp, 0.4),
            (str(gesture_count), 0.2),
            ("Normal" if gesture_count < 3 else "Atención", 0.25)
        ]
        
        for text, width in data:
            label = Label(
                text=text,
                font_size=12,
                size_hint_x=width,
                color=(0, 0, 0, 1),
                halign='center',
                valign='middle'
            )
            container.add_widget(label)
        
        return container
    
    def display_nod_reports(self):
        """
        Muestra los reportes de cabeceo
        """
        try:
            reports_container = self.ids.reports_container
            reports_container.clear_widgets()
            
            if not self.reports_data:
                self.display_no_data_message()
                return
            
            # Crear encabezado simple
            header_label = Label(
                text="Reportes de Cabeceo",
                font_size=16,
                bold=True,
                size_hint_y=None,
                height=dp(30),
                color=(0.2, 0.2, 0.2, 1)
            )
            reports_container.add_widget(header_label)
            
            # Mostrar reportes
            for i, report in enumerate(self.reports_data):
                report_widget = self.create_nod_report_widget(report, i + 1)
                reports_container.add_widget(report_widget)
                
        except Exception as e:
            print(f"Error al mostrar reportes de cabeceo: {e}")
            self.display_error_message()
    
    def create_nod_report_widget(self, report, index):
        """
        Crea un widget para un reporte de cabeceo
        """
        container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(35),
            padding=dp(10),
            spacing=dp(10)
        )
        
        # Alternar color de fondo
        bg_color = (0.98, 0.98, 0.98, 1) if index % 2 == 0 else (0.95, 0.95, 0.95, 1)
        
        with container.canvas.before:
            Color(*bg_color)
            container.rect = Rectangle(size=container.size, pos=container.pos)
        
        container.bind(size=self.update_rect, pos=self.update_rect)
        
        # Datos del reporte
        timestamp = report.get('timestamp', 'N/A')
        gesture_count = report.get('gesture_count', 0)
        
        # Crear labels
        data = [
            (str(index), 0.15),
            (timestamp.split('T')[1][:8] if 'T' in timestamp else timestamp, 0.4),
            (str(gesture_count), 0.2),
            ("Normal" if gesture_count < 3 else "Atención", 0.25)
        ]
        
        for text, width in data:
            label = Label(
                text=text,
                font_size=12,
                size_hint_x=width,
                color=(0, 0, 0, 1),
                halign='center',
                valign='middle'
            )
            container.add_widget(label)
        
        return container
    
    def display_no_data_message(self):
        """
        Muestra un mensaje cuando no hay datos
        """
        reports_container = self.ids.reports_container
        reports_container.clear_widgets()
        
        message = Label(
            text="No hay reportes disponibles para este viaje",
            font_size=16,
            halign='center',
            valign='middle',
            color=(0.5, 0.5, 0.5, 1)
        )
        reports_container.add_widget(message)
    
    def display_error_message(self):
        """
        Muestra un mensaje de error
        """
        reports_container = self.ids.reports_container
        reports_container.clear_widgets()
        
        message = Label(
            text="Error al cargar los reportes",
            font_size=16,
            halign='center',
            valign='middle',
            color=(1, 0, 0, 1)
        )
        reports_container.add_widget(message)
    
    def update_rect(self, instance, value):
        """
        Actualiza el rectángulo de fondo
        """
        if hasattr(instance, 'rect'):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
    
    def refresh_reports(self):
        """
        Actualiza los reportes
        """
        print("Actualizando reportes detallados...")
        self.load_detailed_reports()
    
    def go_back(self):
        """
        Regresa a la pantalla anterior
        """
        self.manager.current = 'view_reports_company'