from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle, Line, RoundedRectangle
from kivy.animation import Animation
from database import get_final_reports_by_trip

class ViewReportsAdminScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reports_data = {}
        self.current_driver = None
        # Colores del tema
        self.colors = {
            'background': (255/255, 252/255, 242/255, 1),  # #FFFCF2
            'surface': (204/255, 197/255, 185/255, 1),     # #CCC5B9
            'primary': (168/255, 159/255, 145/255, 1),     # #A89F91
            'border': (20/255, 26/255, 28/255, 1),         # #141A1C
            'text': (20/255, 26/255, 28/255, 1),           # #141A1C
            'text_secondary': (20/255, 26/255, 28/255, 0.7)
        }
    
    def on_enter(self):
        """
        Se ejecuta cuando entramos a la pantalla
        """
        # Animación de entrada suave
        self.opacity = 0
        Animation(opacity=1, duration=0.3).start(self)
        
        self.load_driver_reports()
    
    def load_driver_reports(self):
        """
        Carga los reportes finales del conductor seleccionado
        """
        try:
            # Obtener el conductor seleccionado
            self.current_driver = App.get_running_app().selected_driver
            
            if not self.current_driver:
                print("Error: No hay conductor seleccionado")
                self.ids.status_label.text = "Error: No hay conductor seleccionado"
                return
            
            driver_id = self.current_driver.get('id')
            driver_name = self.current_driver.get('name')
            
            print(f"Cargando reportes para: {driver_name} (ID: {driver_id})")
            self.ids.status_label.text = "Cargando reportes..."
            
            # Obtener el trip_id seleccionado
            trip_id = App.get_running_app().selected_trip_id
            
            if not trip_id:
                print("Error: No hay viaje seleccionado")
                self.ids.status_label.text = "Error: No hay viaje seleccionado"
                return
            
            # Obtener reportes de la base de datos
            self.reports_data = get_final_reports_by_trip(trip_id)
            print(f"Reportes obtenidos: {self.reports_data}")
            
            # Actualizar la interfaz
            self.update_reports_display()
            
        except Exception as e:
            print(f"Error al cargar reportes: {e}")
            import traceback
            traceback.print_exc()
            self.reports_data = {}
            self.ids.status_label.text = "Error al cargar reportes"
            self.update_reports_display()
    
    def update_reports_display(self):
        """
        Actualiza la visualización de los reportes
        """
        try:
            # Actualizar el título con el nombre del conductor
            if self.current_driver:
                self.ids.driver_name_label.text = f"Reportes de {self.current_driver.get('name', 'N/A')}"
            
            # Limpiar la lista actual
            reports_list = self.ids.reports_list
            reports_list.clear_widgets()
            
            if not self.reports_data:
                # Si no hay reportes, mostrar mensaje
                self.ids.status_label.text = "No se encontraron reportes para este viaje"
                no_reports_widget = self.create_no_reports_widget()
                reports_list.add_widget(no_reports_widget)
                return
            
            # Crear widgets para cada tipo de reporte
            self.create_reports_widgets(reports_list)
            
            # Actualizar status
            total_report_types = len([k for k, v in self.reports_data.items() if v])
            self.ids.status_label.text = f"Se encontraron {total_report_types} tipos de reportes"
                
        except Exception as e:
            print(f"Error al actualizar visualización de reportes: {e}")
            import traceback
            traceback.print_exc()
            self.ids.status_label.text = "Error al mostrar reportes"
    
    def create_no_reports_widget(self):
        """
        Crea un widget para mostrar cuando no hay reportes
        """
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(150),
            padding=dp(30),
            spacing=dp(15)
        )

        with container.canvas.before:
            Color(*self.colors['surface'])
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

        # Mensaje principal
        message_label = Label(
            text="No hay reportes disponibles",
            font_size=sp(18),
            bold=True,
            halign='center',
            valign='middle',
            color=self.colors['text'],
            size_hint_y=None,
            height=dp(30)
        )

        # Submensaje
        sub_label = Label(
            text="Los reportes aparecerán aquí una vez que se registren gestos durante el viaje",
            font_size=sp(14),
            halign='center',
            valign='middle',
            color=self.colors['text_secondary'],
            size_hint_y=None,
            height=dp(40),
            italic=True,
            text_size=(None, None)
        )
        sub_label.bind(size=sub_label.setter('text_size'))

        container.add_widget(message_label)
        container.add_widget(sub_label)

        return container
    
    def create_reports_widgets(self, reports_list):
        """
        Crea widgets para cada tipo de reporte con animación escalonada
        """
        # Orden de los reportes para mostrar
        report_types = [
            ('blink_reports', 'Reportes de Parpadeo', 'normal_reports', 'risk_reports', 'blink'),
            ('yawn_reports', 'Reportes de Bostezos', 'normal_reports', 'risk_reports', 'yawn'),
            ('eye_rub_reports', 'Reportes de Frotamiento de Ojos', 'gesture_count', None, None),
            ('nod_reports', 'Reportes de Cabeceo', 'gesture_count', None, None)
        ]
        
        animation_delay = 0
        for report_key, report_title, normal_key, risk_key, detail_type in report_types:
            reports = self.reports_data.get(report_key, [])
            if reports:  # Solo mostrar si hay reportes
                report_widget = self.create_report_type_widget(report_title, reports, normal_key, risk_key, detail_type)
                reports_list.add_widget(report_widget)
                
                # Animación escalonada
                report_widget.opacity = 0
                Animation(opacity=1, duration=0.3, t='out_cubic').start(report_widget)
                animation_delay += 0.1
    
    def create_report_type_widget(self, title, reports, normal_key, risk_key, detail_type):
        """
        Crea un widget profesional para un tipo específico de reporte
        """
        # Calcular altura dinámica basada en el contenido
        base_height = dp(180)  # Altura base
        additional_height = min(len(reports), 3) * dp(35)  # Máximo 3 reportes mostrados
        total_height = base_height + additional_height
        
        # Contenedor principal
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=total_height,
            padding=dp(18),
            spacing=dp(12)
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
        
        # Header del reporte
        header_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(30),
            spacing=dp(10)
        )
        
        # Título del tipo de reporte
        title_label = Label(
            text=title,
            font_size=sp(18),
            bold=True,
            halign='left',
            valign='middle',
            color=self.colors['text'],
            size_hint_x=0.7,
            text_size=(None, None)
        )
        title_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        
        # Badge con cantidad
        badge_label = Label(
            text=f"{len(reports)}",
            font_size=sp(16),
            bold=True,
            halign='center',
            valign='middle',
            color=self.colors['text'],
            size_hint_x=None,
            width=dp(40),
            size_hint_y=None,
            height=dp(25)
        )
        
        with badge_label.canvas.before:
            Color(*self.colors['primary'])
            badge_label.bg_rect = RoundedRectangle(
                pos=badge_label.pos,
                size=badge_label.size,
                radius=[dp(12)]
            )
            Color(*self.colors['border'])
            badge_label.border_line = Line(
                width=dp(1),
                rounded_rectangle=(badge_label.x, badge_label.y, badge_label.width, badge_label.height, dp(12))
            )
        
        badge_label.bind(size=self.update_button_canvas, pos=self.update_button_canvas)
        
        header_container.add_widget(title_label)
        header_container.add_widget(badge_label)
        
        # Estadísticas generales
        stats_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(5)
        )
        
        total_reports = len(reports)
        total_normal = sum(report.get(normal_key, 0) for report in reports)
        total_risk = sum(report.get(risk_key, 0) for report in reports) if risk_key else 0
        
        stats_text_1 = f"Total de registros: {total_reports}"
        
        if risk_key:
            stats_text_2 = f"Normales: {total_normal} | Riesgo: {total_risk}"
        else:
            stats_text_2 = f"Gestos detectados: {total_normal}"
        
        stats_label_1 = Label(
            text=stats_text_1,
            font_size=sp(14),
            halign='left',
            valign='middle',
            color=self.colors['text_secondary'],
            size_hint_y=None,
            height=dp(22),
            text_size=(None, None)
        )
        stats_label_1.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        
        stats_label_2 = Label(
            text=stats_text_2,
            font_size=sp(14),
            halign='left',
            valign='middle',
            color=self.colors['text_secondary'],
            size_hint_y=None,
            height=dp(22),
            text_size=(None, None)
        )
        stats_label_2.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        
        stats_container.add_widget(stats_label_1)
        stats_container.add_widget(stats_label_2)
        
        # Lista de reportes individuales (mostrar solo los primeros 3)
        reports_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(35) * min(len(reports), 3),
            spacing=dp(5)
        )
        
        reports_to_show = reports[:3]  # Limitar a 3 reportes
        
        for i, report in enumerate(reports_to_show):
            report_item = self.create_individual_report_widget(report, normal_key, risk_key, i+1)
            reports_container.add_widget(report_item)
        
        # Contenedor de botones
        button_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10),
            padding=[dp(0), dp(5), dp(0), dp(0)]
        )
        
        # Indicador si hay más reportes
        if len(reports) > 3:
            more_label = Label(
                text=f"... y {len(reports) - 3} más",
                font_size=sp(12),
                halign='left',
                valign='middle',
                color=self.colors['text_secondary'],
                italic=True,
                size_hint_x=0.6,
                text_size=(None, None)
            )
            more_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
            button_container.add_widget(more_label)
        else:
            spacer = Label(size_hint_x=0.6)
            button_container.add_widget(spacer)
        
        # Botón "Ver Detalles" solo para blink y yawn
        if detail_type in ['blink', 'yawn']:
            details_button = Button(
                text="Ver Detalles",
                size_hint_x=0.4,
                size_hint_y=None,
                height=dp(32),
                font_size=sp(12),
                bold=True,
                background_normal='',
                background_color=(0, 0, 0, 0),
                color=self.colors['text']
            )
            
            with details_button.canvas.before:
                Color(*self.colors['primary'])
                details_button.bg_rect = RoundedRectangle(
                    pos=details_button.pos,
                    size=details_button.size,
                    radius=[dp(16)]
                )
                Color(*self.colors['border'])
                details_button.border_line = Line(
                    width=dp(1),
                    rounded_rectangle=(
                        details_button.x, details_button.y, 
                        details_button.width, details_button.height, 
                        dp(16)
                    )
                )
            
            details_button.bind(
                size=self.update_button_canvas,
                pos=self.update_button_canvas,
                on_press=lambda x, dt=detail_type: self.view_detailed_reports(dt)
            )
            
            button_container.add_widget(details_button)
        
        # Agregar todos los elementos al contenedor principal
        container.add_widget(header_container)
        container.add_widget(stats_container)
        container.add_widget(reports_container)
        container.add_widget(button_container)
        
        return container
    
    def create_individual_report_widget(self, report, normal_key, risk_key, index):
        """
        Crea un widget compacto para un reporte individual
        """
        container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(30),
            spacing=dp(10)
        )
        
        # Número del reporte
        index_label = Label(
            text=f"{index}.",
            font_size=sp(13),
            size_hint_x=None,
            width=dp(25),
            halign='center',
            valign='middle',
            color=self.colors['text'],
            bold=True
        )
        
        # Información del reporte
        if risk_key:
            info_text = f"Normal: {report.get(normal_key, 0)}, Riesgo: {report.get(risk_key, 0)}"
            if report.get('risk_level'):
                info_text += f", Nivel: {report.get('risk_level', 'N/A')}"
        else:
            info_text = f"Gestos: {report.get(normal_key, 0)}"
        
        info_label = Label(
            text=info_text,
            font_size=sp(12),
            halign='left',
            valign='middle',
            color=self.colors['text_secondary'],
            text_size=(None, None)
        )
        info_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value - dp(20), None)))
        
        # Fecha del reporte (formato compacto)
        created_at = report.get('created_at', 'N/A')
        if created_at != 'N/A':
            try:
                date_parts = created_at.split('T')[0] if 'T' in created_at else created_at
                date_text = date_parts
            except:
                date_text = created_at
        else:
            date_text = "N/A"
        
        date_label = Label(
            text=date_text,
            font_size=sp(11),
            halign='right',
            valign='middle',
            color=self.colors['text_secondary'],
            size_hint_x=None,
            width=dp(80),
            italic=True
        )
        
        container.add_widget(index_label)
        container.add_widget(info_label)
        container.add_widget(date_label)
        
        return container
    
    def view_detailed_reports(self, detail_type):
        """
        Navega a la pantalla de reportes detallados
        """
        try:
            app = App.get_running_app()
            app.selected_report_type = detail_type
            
            # Obtener el trip_id del viaje actual
            trip_id = None
            
            # Buscar en los reportes del tipo seleccionado
            report_types = ['blink_reports', 'yawn_reports', 'eye_rub_reports', 'nod_reports']
            
            for report_type in report_types:
                reports = self.reports_data.get(report_type, [])
                if reports and len(reports) > 0:
                    trip_id = reports[0].get('trip_id')
                    break
            
            # Si no encontramos trip_id, usar el que ya tenemos en la app
            if not trip_id:
                trip_id = getattr(app, 'selected_trip_id', None)
            
            app.selected_trip_id = trip_id
            
            print(f"Navegando a reportes detallados - Tipo: {detail_type}, Trip ID: {trip_id}")
            
            if trip_id:
                # Animación de salida
                Animation(opacity=0, duration=0.2).start(self)
                self.manager.current = 'view_detailed_reports_admin'
            else:
                print("Error: No se pudo determinar el trip_id para los reportes detallados")
                self.ids.status_label.text = "Error: No se pudo acceder a los detalles"
                
        except Exception as e:
            print(f"Error al navegar a reportes detallados: {e}")
            import traceback
            traceback.print_exc()
            self.ids.status_label.text = "Error al acceder a los detalles"
    
    def update_canvas_rect(self, instance, value):
        """
        Actualiza el canvas cuando cambia el tamaño del widget
        """
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
        if hasattr(instance, 'border_line'):
            instance.border_line.rounded_rectangle = (
                instance.x, instance.y, instance.width, instance.height, dp(12)
            )

    def update_button_canvas(self, instance, value):
        """
        Actualiza el canvas del botón cuando cambia el tamaño
        """
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
        if hasattr(instance, 'border_line'):
            instance.border_line.rounded_rectangle = (
                instance.x, instance.y, instance.width, instance.height, dp(16)
            )
    
    def refresh_reports(self):
        """
        Actualiza los reportes del conductor
        """
        print("Actualizando reportes del conductor...")
        self.ids.status_label.text = "Actualizando..."
        self.load_driver_reports()
    
    def go_back(self):
        """
        Regresa a la pantalla de viajes
        """
        try:
            print("Regresando a la pantalla de viajes...")
            # Animación de salida
            Animation(opacity=0, duration=0.2).start(self)
            self.manager.current = 'view_trips_admin'
        except Exception as e:
            print(f"Error al regresar: {e}")
            import traceback
            traceback.print_exc()