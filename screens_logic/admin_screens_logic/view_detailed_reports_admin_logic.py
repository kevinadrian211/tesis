from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from database import supabase

class ViewDetailedReportsAdminScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.detailed_reports = []
        self.current_driver = None
        self.current_trip_id = None
        self.report_type = None  # 'blink' o 'yawn'
    
    def on_enter(self):
        """
        Se ejecuta cuando entramos a la pantalla
        """
        self.load_detailed_reports()
    
    def load_detailed_reports(self):
        """
        Carga los reportes detallados según el tipo seleccionado
        """
        try:
            app = App.get_running_app()
            self.current_driver = app.selected_driver
            self.current_trip_id = getattr(app, 'selected_trip_id', None)
            self.report_type = getattr(app, 'selected_report_type', None)
            
            if not self.current_driver or not self.current_trip_id or not self.report_type:
                print("Error: Faltan datos necesarios para cargar reportes detallados")
                self.detailed_reports = []
                self.update_display()
                return
            
            driver_id = self.current_driver.get('id')
            driver_name = self.current_driver.get('name')
            
            print(f"Cargando reportes detallados para: {driver_name} (ID: {driver_id})")
            print(f"Trip ID: {self.current_trip_id}, Tipo: {self.report_type}")
            
            # Cargar reportes según el tipo
            if self.report_type == 'blink':
                self.detailed_reports = self.get_blink_minute_reports(driver_id, self.current_trip_id)
            elif self.report_type == 'yawn':
                self.detailed_reports = self.get_yawn_detailed_reports(driver_id, self.current_trip_id)
            
            print(f"Reportes detallados obtenidos: {len(self.detailed_reports)}")
            
            # Actualizar la interfaz
            self.update_display()
            
        except Exception as e:
            print(f"Error al cargar reportes detallados: {e}")
            import traceback
            traceback.print_exc()
            self.detailed_reports = []
            self.update_display()
    
    def get_blink_minute_reports(self, driver_id, trip_id):
        """
        Obtiene los reportes de parpadeo por minuto
        """
        try:
            response = supabase.table('blink_minute_reports').select('*').eq('driver_id', driver_id).eq('trip_id', trip_id).order('timestamp', desc=False).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error al obtener reportes de parpadeo por minuto: {e}")
            return []
    
    def get_yawn_detailed_reports(self, driver_id, trip_id):
        """
        Obtiene los reportes de bostezos de 5 y 10 minutos
        """
        try:
            reports = []
            
            # Obtener reportes de 5 minutos
            response_5min = supabase.table('yawn_5min_reports').select('*').eq('driver_id', driver_id).eq('trip_id', trip_id).order('timestamp', desc=False).execute()
            if response_5min.data:
                for report in response_5min.data:
                    report['interval_type'] = '5 minutos'
                    reports.append(report)
            
            # Obtener reportes de 10 minutos
            response_10min = supabase.table('yawn_10min_reports').select('*').eq('driver_id', driver_id).eq('trip_id', trip_id).order('timestamp', desc=False).execute()
            if response_10min.data:
                for report in response_10min.data:
                    report['interval_type'] = '10 minutos'
                    reports.append(report)
            
            # Ordenar por timestamp
            reports.sort(key=lambda x: x.get('timestamp', ''))
            
            return reports
            
        except Exception as e:
            print(f"Error al obtener reportes de bostezos detallados: {e}")
            return []
    
    def update_display(self):
        """
        Actualiza la visualización de los reportes detallados
        """
        try:
            # Actualizar el título
            if self.current_driver:
                driver_name = self.current_driver.get('name', 'N/A')
                report_title = "Parpadeo" if self.report_type == 'blink' else "Bostezos"
                self.ids.title_label.text = f"Reportes Detallados de {report_title} - {driver_name}"
            
            # Limpiar la lista actual
            details_list = self.ids.details_list
            details_list.clear_widgets()
            
            if not self.detailed_reports:
                # Si no hay reportes, mostrar mensaje
                no_reports_widget = self.create_no_reports_widget()
                details_list.add_widget(no_reports_widget)
                return
            
            # Crear widgets para cada reporte
            for i, report in enumerate(self.detailed_reports):
                report_widget = self.create_detailed_report_widget(report, i + 1)
                details_list.add_widget(report_widget)
                
        except Exception as e:
            print(f"Error al actualizar visualización de reportes detallados: {e}")
            import traceback
            traceback.print_exc()
    
    def create_no_reports_widget(self):
        """
        Crea un widget para mostrar cuando no hay reportes
        """
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            padding=dp(20)
        )
        
        # Crear fondo con color
        with container.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Gris claro
            container.rect = Rectangle(size=container.size, pos=container.pos)
        
        # Actualizar el rectángulo cuando cambie el tamaño
        container.bind(size=self.update_rect, pos=self.update_rect)
        
        message_label = Label(
            text="No hay reportes detallados disponibles",
            font_size=16,
            halign='center',
            valign='middle',
            color=(0.5, 0.5, 0.5, 1)
        )
        
        container.add_widget(message_label)
        return container
    
    def create_detailed_report_widget(self, report, index):
        """
        Crea un widget para un reporte detallado
        """
        # Contenedor principal
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(15),
            spacing=dp(8)
        )
        
        # Crear fondo con borde
        with container.canvas.before:
            Color(0.98, 0.98, 0.98, 1)  # Fondo muy claro
            container.rect = Rectangle(size=container.size, pos=container.pos)
            Color(0.7, 0.7, 0.7, 1)  # Borde gris
            container.border = Rectangle(size=container.size, pos=container.pos)
        
        # Actualizar el rectángulo cuando cambie el tamaño
        container.bind(size=self.update_rect, pos=self.update_rect)
        
        # Título con número de reporte
        title_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(25)
        )
        
        title_label = Label(
            text=f"Reporte #{index}",
            font_size=16,
            bold=True,
            halign='left',
            valign='middle',
            color=(0.2, 0.2, 0.2, 1)
        )
        
        # Timestamp
        timestamp = report.get('timestamp', 'N/A')
        if timestamp != 'N/A':
            try:
                # Formatear timestamp
                if 'T' in timestamp:
                    date_part, time_part = timestamp.split('T')
                    time_part = time_part.split('.')[0]  # Remover microsegundos
                    formatted_time = f"{date_part} {time_part}"
                else:
                    formatted_time = timestamp
            except:
                formatted_time = timestamp
        else:
            formatted_time = "N/A"
        
        timestamp_label = Label(
            text=formatted_time,
            font_size=12,
            halign='right',
            valign='middle',
            color=(0.5, 0.5, 0.5, 1),
            size_hint_x=None,
            width=dp(150)
        )
        
        title_container.add_widget(title_label)
        title_container.add_widget(timestamp_label)
        container.add_widget(title_container)
        
        # Información específica según el tipo
        if self.report_type == 'blink':
            info_widget = self.create_blink_info_widget(report)
        else:
            info_widget = self.create_yawn_info_widget(report)
        
        container.add_widget(info_widget)
        
        return container
    
    def create_blink_info_widget(self, report):
        """
        Crea el widget de información para reportes de parpadeo
        """
        info_container = BoxLayout(
            orientation='vertical',
            spacing=dp(3)
        )
        
        # Primera línea: Conteo y duración promedio
        line1 = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(20)
        )
        
        count_label = Label(
            text=f"Parpadeos: {report.get('blink_count', 0)}",
            font_size=14,
            halign='left',
            valign='middle',
            color=(0.3, 0.3, 0.3, 1)
        )
        
        duration_label = Label(
            text=f"Duración promedio: {report.get('blink_avg_duration', 0):.2f}s",
            font_size=14,
            halign='right',
            valign='middle',
            color=(0.3, 0.3, 0.3, 1)
        )
        
        line1.add_widget(count_label)
        line1.add_widget(duration_label)
        info_container.add_widget(line1)
        
        # Segunda línea: Comentario e intervalo
        line2 = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(20)
        )
        
        comment_label = Label(
            text=f"Comentario: {report.get('blink_comment', 'N/A')}",
            font_size=12,
            halign='left',
            valign='middle',
            color=(0.4, 0.4, 0.4, 1)
        )
        
        interval_label = Label(
            text=f"Intervalo: {report.get('report_interval_minutes', 1)} min",
            font_size=12,
            halign='right',
            valign='middle',
            color=(0.4, 0.4, 0.4, 1)
        )
        
        line2.add_widget(comment_label)
        line2.add_widget(interval_label)
        info_container.add_widget(line2)
        
        return info_container
    
    def create_yawn_info_widget(self, report):
        """
        Crea el widget de información para reportes de bostezos
        """
        info_container = BoxLayout(
            orientation='vertical',
            spacing=dp(3)
        )
        
        # Primera línea: Conteo y duración promedio
        line1 = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(20)
        )
        
        count_label = Label(
            text=f"Bostezos: {report.get('yawn_count', 0)}",
            font_size=14,
            halign='left',
            valign='middle',
            color=(0.3, 0.3, 0.3, 1)
        )
        
        duration_text = "N/A"
        if report.get('avg_duration'):
            duration_text = f"{float(report.get('avg_duration')):.2f}s"
        
        duration_label = Label(
            text=f"Duración promedio: {duration_text}",
            font_size=14,
            halign='right',
            valign='middle',
            color=(0.3, 0.3, 0.3, 1)
        )
        
        line1.add_widget(count_label)
        line1.add_widget(duration_label)
        info_container.add_widget(line1)
        
        # Segunda línea: Comentario e intervalo
        line2 = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(20)
        )
        
        comment_label = Label(
            text=f"Estado: {report.get('comment', 'N/A')}",
            font_size=12,
            halign='left',
            valign='middle',
            color=(0.4, 0.4, 0.4, 1)
        )
        
        interval_label = Label(
            text=f"Intervalo: {report.get('interval_type', 'N/A')}",
            font_size=12,
            halign='right',
            valign='middle',
            color=(0.4, 0.4, 0.4, 1)
        )
        
        line2.add_widget(comment_label)
        line2.add_widget(interval_label)
        info_container.add_widget(line2)
        
        return info_container
    
    def update_rect(self, instance, value):
        """
        Actualiza el rectángulo de fondo cuando cambia el tamaño del widget
        """
        if hasattr(instance, 'rect'):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
        if hasattr(instance, 'border'):
            instance.border.pos = instance.pos
            instance.border.size = instance.size
    
    def go_back(self):
        """
        Regresa a la pantalla de reportes del conductor
        """
        self.manager.current = 'view_reports_admin'