from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.animation import Animation
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
        # Sistema de colores obligatorio
        self.colors = {
            'background': (255/255, 252/255, 242/255, 1),  # #FFFCF2
            'surface': (204/255, 197/255, 185/255, 1),     # #CCC5B9
            'primary': (168/255, 159/255, 145/255, 1),     # #A89F91
            'border': (20/255, 26/255, 28/255, 1),         # #141A1C
            'text': (20/255, 26/255, 28/255, 1),           # #141A1C
            'text_secondary': (20/255, 26/255, 28/255, 0.7)
        }
        
        self.current_trip_id = None
        self.current_report_type = None
        self.reports_data = []
        self.current_driver = None
        
    def on_enter(self):
        """Animación de entrada y carga de datos"""
        self.load_screen_data()
        self.opacity = 0
        Animation(opacity=1, duration=0.3).start(self)
        
    def load_screen_data(self):
        """Carga los datos necesarios para la pantalla"""
        try:
            app = App.get_running_app()
            self.current_report_type = getattr(app, 'selected_report_type', None)
            self.current_trip_id = getattr(app, 'selected_trip_id', None)
            self.current_driver = getattr(app, 'selected_driver', None)
            
            print(f"Cargando reportes detallados - Tipo: {self.current_report_type}, Trip ID: {self.current_trip_id}")
            
            self.update_screen_info()
            self.load_detailed_reports()
            
        except Exception as e:
            print(f"Error al cargar datos de la pantalla: {e}")
            import traceback
            traceback.print_exc()
    
    def update_screen_info(self):
        """Actualiza la información general de la pantalla"""
        try:
            # Actualizar título según el tipo de reporte
            title_text = "Reportes Detallados"
            if self.current_report_type == 'blink':
                title_text = "Reportes - Parpadeos"
            elif self.current_report_type == 'yawn':
                title_text = "Reportes - Bostezos"
            elif self.current_report_type == 'eye_rub':
                title_text = "Reportes - Frotamiento"
            elif self.current_report_type == 'nod':
                title_text = "Reportes - Cabeceo"
            
            self.ids.title_label.text = title_text
                
        except Exception as e:
            print(f"Error al actualizar información de pantalla: {e}")
    
    def load_detailed_reports(self):
        """Carga los reportes detallados según el tipo seleccionado"""
        try:
            if not self.current_trip_id:
                self.load_all_reports_for_driver()
                return
            
            if self.current_report_type == 'blink':
                self.reports_data = get_minute_reports_by_trip(self.current_trip_id)
                self.display_blink_reports()
            elif self.current_report_type == 'yawn':
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
        """Carga todos los reportes del conductor para el tipo seleccionado"""
        try:
            if not self.current_driver:
                print("Error: No hay conductor seleccionado")
                self.display_no_data_message()
                return
            
            app = App.get_running_app()
            selected_trip_id = getattr(app, 'selected_trip_id_for_driver', None)
            
            if not selected_trip_id:
                print("Error: No hay viaje seleccionado para el conductor")
                self.display_no_data_message()
                return
            
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
        """Muestra los reportes de parpadeo por minuto"""
        try:
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
        """Crea el encabezado para los reportes de parpadeo"""
        header_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            padding=dp(15),
            spacing=dp(8)
        )
        
        with header_container.canvas.before:
            Color(*self.colors['primary'])
            header_container.bg_rect = RoundedRectangle(
                size=header_container.size, 
                pos=header_container.pos, 
                radius=[dp(8)]
            )
            Color(*self.colors['border'])
            header_container.border_line = Line(
                width=dp(1),
                rounded_rectangle=(header_container.x, header_container.y, 
                                header_container.width, header_container.height, dp(8))
            )
        
        header_container.bind(size=self.update_canvas_rect, pos=self.update_canvas_rect)
        
        # Headers con anchos optimizados para móvil
        headers = ["#", "Hora", "Count", "Duración", "Estado"]
        widths = [0.1, 0.25, 0.2, 0.25, 0.2]
        
        for header, width in zip(headers, widths):
            label = Label(
                text=header,
                font_size=sp(14),
                bold=True,
                size_hint_x=width,
                color=self.colors['text'],
                halign='center',
                valign='middle',
                text_size=(None, None)
            )
            label.bind(size=label.setter('text_size'))
            header_container.add_widget(label)
        
        return header_container
    
    def create_blink_report_widget(self, report, index):
        """Crea un widget para un reporte de parpadeo individual"""
        container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(45),
            padding=dp(15),
            spacing=dp(8)
        )
        
        with container.canvas.before:
            Color(*self.colors['background'])
            container.bg_rect = RoundedRectangle(
                size=container.size, 
                pos=container.pos, 
                radius=[dp(8)]
            )
            Color(*self.colors['border'])
            container.border_line = Line(
                width=dp(1),
                rounded_rectangle=(container.x, container.y, 
                                container.width, container.height, dp(8))
            )
        
        container.bind(size=self.update_canvas_rect, pos=self.update_canvas_rect)
        
        # Datos del reporte
        timestamp = report.get('timestamp', 'N/A')
        blink_count = report.get('blink_count', 0)
        avg_duration = report.get('blink_avg_duration', 0)
        
        # Determinar estado y color
        if blink_count > 20:
            status = "Normal"
            status_color = (0, 0.6, 0, 1)
        elif blink_count < 10:
            status = "Atención"
            status_color = (0.8, 0.4, 0, 1)
        else:
            status = "Riesgo"
            status_color = (0.8, 0, 0, 1)
        
        # Formatear hora para móvil
        formatted_time = timestamp.split('T')[1][:5] if 'T' in timestamp else timestamp[:5]
        
        # Crear labels con texto más compacto
        data = [
            (str(index), 0.1, self.colors['text']),
            (formatted_time, 0.25, self.colors['text']),
            (str(blink_count), 0.2, self.colors['text']),
            (f"{avg_duration:.1f}s", 0.25, self.colors['text']),
            (status, 0.2, status_color)
        ]
        
        for text, width, color in data:
            label = Label(
                text=text,
                font_size=sp(12),
                size_hint_x=width,
                color=color,
                halign='center',
                valign='middle',
                text_size=(None, None)
            )
            label.bind(size=label.setter('text_size'))
            container.add_widget(label)
        
        return container
    
    def display_yawn_reports(self, reports_5min, reports_10min):
        """Muestra los reportes de bostezos (5 y 10 minutos)"""
        try:
            reports_container = self.ids.reports_container
            reports_container.clear_widgets()
            
            # Título para reportes de 5 minutos
            if reports_5min:
                title_5min = self.create_section_title("Reportes de 5 Minutos")
                reports_container.add_widget(title_5min)
                
                for i, report in enumerate(reports_5min):
                    report_widget = self.create_yawn_report_widget(report, i + 1)
                    reports_container.add_widget(report_widget)
            
            # Título para reportes de 10 minutos
            if reports_10min:
                title_10min = self.create_section_title("Reportes de 10 Minutos")
                reports_container.add_widget(title_10min)
                
                for i, report in enumerate(reports_10min):
                    report_widget = self.create_yawn_report_widget(report, i + 1)
                    reports_container.add_widget(report_widget)
            
            if not reports_5min and not reports_10min:
                self.display_no_data_message()
                
        except Exception as e:
            print(f"Error al mostrar reportes de bostezos: {e}")
            self.display_error_message()
    
    def create_section_title(self, title_text):
        """Crea un título de sección"""
        title_container = BoxLayout(
            size_hint_y=None,
            height=dp(40),
            padding=[dp(15), dp(8)]
        )
        
        with title_container.canvas.before:
            Color(*self.colors['surface'])
            title_container.bg_rect = RoundedRectangle(
                size=title_container.size, 
                pos=title_container.pos, 
                radius=[dp(6)]
            )
            Color(*self.colors['border'])
            title_container.border_line = Line(
                width=dp(1),
                rounded_rectangle=(title_container.x, title_container.y, 
                                title_container.width, title_container.height, dp(6))
            )
        
        title_container.bind(size=self.update_canvas_rect, pos=self.update_canvas_rect)
        
        title_label = Label(
            text=title_text,
            font_size=sp(16),
            bold=True,
            color=self.colors['text'],
            halign='center',
            valign='middle'
        )
        
        title_container.add_widget(title_label)
        return title_container
    
    def create_yawn_report_widget(self, report, index):
        """Crea un widget para un reporte de bostezo"""
        container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(45),
            padding=dp(15),
            spacing=dp(8)
        )
        
        with container.canvas.before:
            Color(*self.colors['background'])
            container.bg_rect = RoundedRectangle(
                size=container.size, 
                pos=container.pos, 
                radius=[dp(8)]
            )
            Color(*self.colors['border'])
            container.border_line = Line(
                width=dp(1),
                rounded_rectangle=(container.x, container.y, 
                                container.width, container.height, dp(8))
            )
        
        container.bind(size=self.update_canvas_rect, pos=self.update_canvas_rect)
        
        # Datos del reporte
        timestamp = report.get('timestamp', 'N/A')
        yawn_count = report.get('yawn_count', 0)
        avg_duration = report.get('yawn_avg_duration', 0)
        
        formatted_time = timestamp.split('T')[1][:5] if 'T' in timestamp else timestamp[:5]
        status = "Normal" if yawn_count < 3 else "Atención"
        
        # Crear labels
        data = [
            (str(index), 0.15, self.colors['text']),
            (formatted_time, 0.3, self.colors['text']),
            (str(yawn_count), 0.2, self.colors['text']),
            (f"{avg_duration:.1f}s", 0.2, self.colors['text']),
            (status, 0.15, self.colors['text'])
        ]
        
        for text, width, color in data:
            label = Label(
                text=text,
                font_size=sp(12),
                size_hint_x=width,
                color=color,
                halign='center',
                valign='middle',
                text_size=(None, None)
            )
            label.bind(size=label.setter('text_size'))
            container.add_widget(label)
        
        return container
    
    def display_eye_rub_reports(self):
        """Muestra los reportes de frotamiento de ojos"""
        try:
            reports_container = self.ids.reports_container
            reports_container.clear_widgets()
            
            if not self.reports_data:
                self.display_no_data_message()
                return
            
            # Crear título de sección
            title = self.create_section_title("Reportes de Frotamiento de Ojos")
            reports_container.add_widget(title)
            
            # Mostrar reportes
            for i, report in enumerate(self.reports_data):
                report_widget = self.create_eye_rub_report_widget(report, i + 1)
                reports_container.add_widget(report_widget)
                
        except Exception as e:
            print(f"Error al mostrar reportes de frotamiento de ojos: {e}")
            self.display_error_message()
    
    def create_eye_rub_report_widget(self, report, index):
        """Crea un widget para un reporte de frotamiento de ojos"""
        return self.create_generic_report_widget(report, index, 'gesture_count')
    
    def display_nod_reports(self):
        """Muestra los reportes de cabeceo"""
        try:
            reports_container = self.ids.reports_container
            reports_container.clear_widgets()
            
            if not self.reports_data:
                self.display_no_data_message()
                return
            
            # Crear título de sección
            title = self.create_section_title("Reportes de Cabeceo")
            reports_container.add_widget(title)
            
            # Mostrar reportes
            for i, report in enumerate(self.reports_data):
                report_widget = self.create_nod_report_widget(report, i + 1)
                reports_container.add_widget(report_widget)
                
        except Exception as e:
            print(f"Error al mostrar reportes de cabeceo: {e}")
            self.display_error_message()
    
    def create_nod_report_widget(self, report, index):
        """Crea un widget para un reporte de cabeceo"""
        return self.create_generic_report_widget(report, index, 'gesture_count')
    
    def create_generic_report_widget(self, report, index, count_field):
        """Crea un widget genérico para reportes simples"""
        container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(45),
            padding=dp(15),
            spacing=dp(8)
        )
        
        with container.canvas.before:
            Color(*self.colors['background'])
            container.bg_rect = RoundedRectangle(
                size=container.size, 
                pos=container.pos, 
                radius=[dp(8)]
            )
            Color(*self.colors['border'])
            container.border_line = Line(
                width=dp(1),
                rounded_rectangle=(container.x, container.y, 
                                container.width, container.height, dp(8))
            )
        
        container.bind(size=self.update_canvas_rect, pos=self.update_canvas_rect)
        
        # Datos del reporte
        timestamp = report.get('timestamp', 'N/A')
        gesture_count = report.get(count_field, 0)
        
        formatted_time = timestamp.split('T')[1][:5] if 'T' in timestamp else timestamp[:5]
        status = "Normal" if gesture_count < 3 else "Atención"
        
        # Crear labels con diseño móvil optimizado
        data = [
            (str(index), 0.15, self.colors['text']),
            (formatted_time, 0.35, self.colors['text']),
            (str(gesture_count), 0.25, self.colors['text']),
            (status, 0.25, self.colors['text'])
        ]
        
        for text, width, color in data:
            label = Label(
                text=text,
                font_size=sp(12),
                size_hint_x=width,
                color=color,
                halign='center',
                valign='middle',
                text_size=(None, None)
            )
            label.bind(size=label.setter('text_size'))
            container.add_widget(label)
        
        return container
    
    def display_no_data_message(self):
        """Muestra un mensaje cuando no hay datos"""
        reports_container = self.ids.reports_container
        reports_container.clear_widgets()
        
        message_container = BoxLayout(
            size_hint_y=None,
            height=dp(80),
            padding=dp(20)
        )
        
        with message_container.canvas.before:
            Color(*self.colors['surface'])
            message_container.bg_rect = RoundedRectangle(
                size=message_container.size, 
                pos=message_container.pos, 
                radius=[dp(12)]
            )
            Color(*self.colors['border'])
            message_container.border_line = Line(
                width=dp(1),
                rounded_rectangle=(message_container.x, message_container.y, 
                                message_container.width, message_container.height, dp(12))
            )
        
        message_container.bind(size=self.update_canvas_rect, pos=self.update_canvas_rect)
        
        message = Label(
            text="No hay reportes disponibles para este viaje",
            font_size=sp(16),
            halign='center',
            valign='middle',
            color=self.colors['text_secondary'],
            text_size=(None, None)
        )
        message.bind(size=message.setter('text_size'))
        message_container.add_widget(message)
        reports_container.add_widget(message_container)
    
    def display_error_message(self):
        """Muestra un mensaje de error"""
        reports_container = self.ids.reports_container
        reports_container.clear_widgets()
        
        error_container = BoxLayout(
            size_hint_y=None,
            height=dp(80),
            padding=dp(20)
        )
        
        with error_container.canvas.before:
            Color(0.9, 0.3, 0.3, 0.2)  # Fondo rojo suave para error
            error_container.bg_rect = RoundedRectangle(
                size=error_container.size, 
                pos=error_container.pos, 
                radius=[dp(12)]
            )
            Color(0.8, 0, 0, 1)  # Borde rojo para error
            error_container.border_line = Line(
                width=dp(1),
                rounded_rectangle=(error_container.x, error_container.y, 
                                error_container.width, error_container.height, dp(12))
            )
        
        error_container.bind(size=self.update_canvas_rect, pos=self.update_canvas_rect)
        
        message = Label(
            text="Error al cargar los reportes",
            font_size=sp(16),
            halign='center',
            valign='middle',
            color=(0.8, 0, 0, 1),  # Texto rojo para error
            text_size=(None, None)
        )
        message.bind(size=message.setter('text_size'))
        error_container.add_widget(message)
        reports_container.add_widget(error_container)
    
    def update_canvas_rect(self, instance, value):
        """Actualiza el canvas de los widgets dinámicos"""
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
        if hasattr(instance, 'border_line'):
            if hasattr(instance.border_line, 'rounded_rectangle'):
                # Para elementos con bordes redondeados
                radius = dp(8)  # Radio por defecto
                if instance.height > dp(60):
                    radius = dp(12)  # Radio mayor para contenedores grandes
                elif instance.height < dp(50):
                    radius = dp(6)   # Radio menor para elementos pequeños
                    
                instance.border_line.rounded_rectangle = (
                    instance.x, instance.y, instance.width, instance.height, radius
                )
            else:
                # Para elementos con bordes rectangulares
                instance.border_line.rectangle = (
                    instance.x, instance.y, instance.width, instance.height
                )
    
    def refresh_reports(self):
        """Actualiza los reportes con animación"""
        print("Actualizando reportes detallados...")
        
        # Animación de salida
        current_container = self.ids.reports_container
        Animation(opacity=0.3, duration=0.2).start(current_container)
        
        # Recargar datos después de la animación
        def reload_after_animation(dt):
            self.load_detailed_reports()
            Animation(opacity=1, duration=0.3).start(current_container)
        
        from kivy.clock import Clock
        Clock.schedule_once(reload_after_animation, 0.25)
    
    def go_back(self):
        """Regresa a la pantalla anterior con animación"""
        Animation(opacity=0, duration=0.2).start(self)
        
        def change_screen(dt):
            self.manager.current = 'view_reports_company'
        
        from kivy.clock import Clock
        Clock.schedule_once(change_screen, 0.25)