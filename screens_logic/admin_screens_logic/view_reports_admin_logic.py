from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle, Line
from database import get_final_reports_by_trip

class ViewReportsAdminScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reports_data = {}
        self.current_driver = None
    
    def on_enter(self):
        """
        Se ejecuta cuando entramos a la pantalla
        """
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
                return
            
            driver_id = self.current_driver.get('id')
            driver_name = self.current_driver.get('name')
            
            print(f"Cargando reportes para: {driver_name} (ID: {driver_id})")
            
            # Obtener el trip_id seleccionado
            trip_id = App.get_running_app().selected_trip_id
            
            if not trip_id:
                print("Error: No hay viaje seleccionado")
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
            self.update_reports_display()
    
    def update_reports_display(self):
        """
        Actualiza la visualización de los reportes
        """
        try:
            # Actualizar el título con el nombre del conductor
            if self.current_driver:
                self.ids.driver_name_label.text = f"Reportes de: {self.current_driver.get('name', 'N/A')}"
            
            # Limpiar la lista actual
            reports_list = self.ids.reports_list
            reports_list.clear_widgets()
            
            if not self.reports_data:
                # Si no hay reportes, mostrar mensaje
                no_reports_widget = self.create_no_reports_widget()
                reports_list.add_widget(no_reports_widget)
                return
            
            # Crear widgets para cada tipo de reporte
            self.create_reports_widgets(reports_list)
                
        except Exception as e:
            print(f"Error al actualizar visualización de reportes: {e}")
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
        
        # Crear fondo blanco con borde negro
        def update_graphics(instance, value):
            instance.canvas.before.clear()
            with instance.canvas.before:
                Color(1, 1, 1, 1)  # Fondo blanco
                Rectangle(size=instance.size, pos=instance.pos)
                Color(0, 0, 0, 1)  # Borde negro
                Line(rectangle=(instance.x, instance.y, instance.width, instance.height), width=1)
        
        container.bind(size=update_graphics, pos=update_graphics)
        # Ejecutar una vez para crear los gráficos iniciales
        update_graphics(container, None)
        
        message_label = Label(
            text="No hay reportes disponibles para este conductor",
            font_size=sp(18),
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1)  # Texto negro
        )
        
        container.add_widget(message_label)
        return container
    
    def create_reports_widgets(self, reports_list):
        """
        Crea widgets para cada tipo de reporte
        """
        # Orden de los reportes para mostrar
        report_types = [
            ('blink_reports', 'Reportes de Parpadeo', 'normal_reports', 'risk_reports', 'blink'),
            ('yawn_reports', 'Reportes de Bostezos', 'normal_reports', 'risk_reports', 'yawn'),
            ('eye_rub_reports', 'Reportes de Frotamiento de Ojos', 'gesture_count', None, None),
            ('nod_reports', 'Reportes de Cabeceo', 'gesture_count', None, None)
        ]
        
        for report_key, report_title, normal_key, risk_key, detail_type in report_types:
            reports = self.reports_data.get(report_key, [])
            if reports:  # Solo mostrar si hay reportes
                report_widget = self.create_report_type_widget(report_title, reports, normal_key, risk_key, detail_type)
                reports_list.add_widget(report_widget)
    
    def create_report_type_widget(self, title, reports, normal_key, risk_key, detail_type):
        """
        Crea un widget para un tipo específico de reporte
        """
        # Contenedor principal
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(200 + len(reports) * 30),  # Altura aumentada para botón
            padding=dp(15),
            spacing=dp(10)
        )
        
        # Crear fondo blanco con borde negro
        def update_graphics(instance, value):
            instance.canvas.before.clear()
            with instance.canvas.before:
                Color(1, 1, 1, 1)  # Fondo blanco
                Rectangle(size=instance.size, pos=instance.pos)
                Color(0, 0, 0, 1)  # Borde negro
                Line(rectangle=(instance.x, instance.y, instance.width, instance.height), width=2)
        
        container.bind(size=update_graphics, pos=update_graphics)
        # Ejecutar una vez para crear los gráficos iniciales
        update_graphics(container, None)
        
        # Título del tipo de reporte
        title_label = Label(
            text=title,
            font_size=sp(20),
            bold=True,
            halign='left',
            valign='middle',
            text_size=(None, None),
            size_hint_y=None,
            height=dp(30),
            color=(0, 0, 0, 1)  # Texto negro
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        container.add_widget(title_label)
        
        # Estadísticas generales
        stats_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(25),
            spacing=dp(20)
        )
        
        total_reports = len(reports)
        total_normal = sum(report.get(normal_key, 0) for report in reports)
        total_risk = sum(report.get(risk_key, 0) for report in reports) if risk_key else 0
        
        stats_label = Label(
            text=f"Total de viajes: {total_reports}",
            font_size=sp(16),
            halign='left',
            valign='middle',
            color=(0, 0, 0, 1)  # Texto negro
        )
        
        if risk_key:
            risk_stats_label = Label(
                text=f"Reportes normales: {total_normal} | Reportes de riesgo: {total_risk}",
                font_size=sp(16),
                halign='left',
                valign='middle',
                color=(0, 0, 0, 1)  # Texto negro
            )
            stats_container.add_widget(stats_label)
            stats_container.add_widget(risk_stats_label)
        else:
            gesture_stats_label = Label(
                text=f"Gestos detectados: {total_normal}",
                font_size=sp(16),
                halign='left',
                valign='middle',
                color=(0, 0, 0, 1)  # Texto negro
            )
            stats_container.add_widget(stats_label)
            stats_container.add_widget(gesture_stats_label)
        
        container.add_widget(stats_container)
        
        # Lista de reportes individuales (mostrar solo los primeros 3)
        reports_to_show = reports[:3]  # Limitar a 3 reportes para no sobrecargar
        
        for i, report in enumerate(reports_to_show):
            report_item = self.create_individual_report_widget(report, normal_key, risk_key, i+1, detail_type)
            container.add_widget(report_item)
        
        # Si hay más reportes, mostrar indicador
        if len(reports) > 3:
            more_label = Label(
                text=f"... y {len(reports) - 3} reportes más",
                font_size=sp(14),
                halign='center',
                valign='middle',
                color=(0.4, 0.4, 0.4, 1),  # Texto gris oscuro
                size_hint_y=None,
                height=dp(20)
            )
            container.add_widget(more_label)
        
        # Botón "Ver Detalles" solo para blink y yawn
        if detail_type in ['blink', 'yawn']:
            details_button = Button(
                text="Ver Detalles",
                size_hint_y=None,
                height=dp(35),
                size_hint_x=None,
                width=dp(150),
                pos_hint={'center_x': 0.5},
                background_color=(1, 1, 1, 1),  # Fondo blanco
                color=(0, 0, 0, 1)  # Texto negro
            )
            
            # Agregar borde negro al botón
            def update_button_graphics(instance, value):
                instance.canvas.before.clear()
                with instance.canvas.before:
                    Color(1, 1, 1, 1)  # Fondo blanco
                    Rectangle(size=instance.size, pos=instance.pos)
                    Color(0, 0, 0, 1)  # Borde negro
                    Line(rectangle=(instance.x, instance.y, instance.width, instance.height), width=1)
            
            details_button.bind(size=update_button_graphics, pos=update_button_graphics)
            details_button.bind(on_press=lambda x, dt=detail_type: self.view_detailed_reports(dt))
            # Ejecutar una vez para crear los gráficos iniciales
            update_button_graphics(details_button, None)
            
            container.add_widget(details_button)
        
        return container
    
    def create_individual_report_widget(self, report, normal_key, risk_key, index, detail_type):
        """
        Crea un widget para un reporte individual
        """
        container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(30),
            spacing=dp(10)
        )
        
        # Agregar fondo blanco con borde sutil
        def update_graphics(instance, value):
            instance.canvas.before.clear()
            with instance.canvas.before:
                Color(0.98, 0.98, 0.98, 1)  # Fondo blanco ligeramente gris
                Rectangle(size=instance.size, pos=instance.pos)
                Color(0, 0, 0, 0.3)  # Borde gris suave
                Line(rectangle=(instance.x, instance.y, instance.width, instance.height), width=1)
        
        container.bind(size=update_graphics, pos=update_graphics)
        update_graphics(container, None)
        
        # Número del reporte
        index_label = Label(
            text=f"{index}.",
            font_size=sp(16),
            size_hint_x=None,
            width=dp(30),
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1)  # Texto negro
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
            font_size=sp(16),
            halign='left',
            valign='middle',
            color=(0, 0, 0, 1)  # Texto negro
        )
        
        # Fecha del reporte
        created_at = report.get('created_at', 'N/A')
        if created_at != 'N/A':
            try:
                # Formatear fecha si es necesario
                date_parts = created_at.split('T')[0] if 'T' in created_at else created_at
                date_text = f"Fecha: {date_parts}"
            except:
                date_text = f"Fecha: {created_at}"
        else:
            date_text = "Fecha: N/A"
        
        date_label = Label(
            text=date_text,
            font_size=sp(14),
            halign='right',
            valign='middle',
            color=(0.3, 0.3, 0.3, 1),  # Texto gris oscuro
            size_hint_x=None,
            width=dp(120)
        )
        
        # Solo agregar los elementos básicos sin el botón "Ver"
        container.add_widget(index_label)
        container.add_widget(info_label)
        container.add_widget(date_label)
        
        return container
    
    def view_detailed_reports(self, detail_type):
        """
        Navega a la pantalla de reportes detallados (vista general)
        """
        try:
            app = App.get_running_app()
            app.selected_report_type = detail_type
            
            # Obtener el trip_id del viaje actual que se está mostrando
            # Usamos el trip_id del primer reporte disponible
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
                self.manager.current = 'view_detailed_reports_admin'
            else:
                print("Error: No se pudo determinar el trip_id para los reportes detallados")
                
        except Exception as e:
            print(f"Error al navegar a reportes detallados: {e}")
            import traceback
            traceback.print_exc()
    
    def update_rect(self, instance, value):
        """
        Actualiza el rectángulo de fondo cuando cambia el tamaño del widget
        """
        # Este método ya no es necesario con el nuevo approach
        pass
    
    def update_button_border(self, instance, value):
        """
        Actualiza el borde del botón cuando cambia el tamaño
        """
        # Este método ya no es necesario con el nuevo approach
        pass
    
    def refresh_reports(self):
        """
        Actualiza los reportes del conductor
        """
        print("Actualizando reportes del conductor...")
        self.load_driver_reports()
    
    def go_back(self):
        """
        Regresa a la pantalla de conductores
        """
        self.manager.current = 'view_trips_admin'