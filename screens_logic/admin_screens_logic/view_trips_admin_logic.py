from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle, Line, RoundedRectangle
from kivy.animation import Animation
from database import get_trips_by_driver

class ViewTripsAdminScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.driver_data = None
        self.trips_data = []
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
        
        self.load_selected_driver()
        if self.driver_data:
            self.load_trips()

    def load_selected_driver(self):
        """
        Carga los datos del conductor seleccionado desde la app
        """
        try:
            app = App.get_running_app()
            self.driver_data = getattr(app, 'selected_driver', None)

            if self.driver_data:
                print(f"Conductor seleccionado: {self.driver_data['name']} (ID: {self.driver_data['id']})")
                # Actualizar el título con el nombre del conductor
                self.ids.title_label.text = f"Viajes de {self.driver_data['name']}"
            else:
                print("No se encontró conductor seleccionado")
                self.ids.title_label.text = "Viajes del Conductor"

        except Exception as e:
            print(f"Error al cargar conductor seleccionado: {e}")
            import traceback
            traceback.print_exc()

    def load_trips(self):
        """
        Carga los viajes del conductor seleccionado
        """
        if not self.driver_data:
            print("No hay conductor seleccionado")
            return

        try:
            self.ids.status_label.text = "Cargando viajes..."
            self.clear_trips()

            # Obtener viajes del conductor
            driver_id = self.driver_data['id']
            print(f"Buscando viajes para conductor ID: {driver_id}")

            self.trips_data = get_trips_by_driver(driver_id)
            print(f"Viajes obtenidos: {len(self.trips_data)}")

            # Debug: Imprimir primeros viajes
            if self.trips_data:
                print("Primeros viajes:")
                for i, trip in enumerate(self.trips_data[:3]):
                    print(f"  {i+1}. {trip.get('start_location', 'N/A')} -> {trip.get('end_location', 'N/A')}")

            # Actualizar la interfaz
            self.update_trips_list()

        except Exception as e:
            print(f"Error al cargar viajes: {e}")
            import traceback
            traceback.print_exc()
            self.trips_data = []
            self.update_trips_list()

    def update_trips_list(self):
        """
        Actualiza la lista visual de viajes
        """
        try:
            # Limpiar la lista actual
            trips_list = self.ids.trips_list
            trips_list.clear_widgets()

            if not self.trips_data:
                # Si no hay viajes, mostrar mensaje
                self.ids.status_label.text = "No se encontraron viajes para este conductor"
                no_trips_widget = self.create_no_trips_widget()
                trips_list.add_widget(no_trips_widget)
                return

            # Actualizar mensaje de estado
            self.ids.status_label.text = f"Se encontraron {len(self.trips_data)} viajes"

            # Crear widgets para cada viaje con animación escalonada
            for i, trip in enumerate(self.trips_data):
                trip_widget = self.create_trip_widget(trip)
                trips_list.add_widget(trip_widget)
                # Animación escalonada para cada elemento
                trip_widget.opacity = 0
                Animation(opacity=1, duration=0.2, t='out_cubic').start(trip_widget)

        except Exception as e:
            print(f"Error al actualizar lista de viajes: {e}")
            import traceback
            traceback.print_exc()
            self.ids.status_label.text = "Error al cargar viajes"

    def create_no_trips_widget(self):
        """
        Crea un widget para mostrar cuando no hay viajes
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
            text="No hay viajes registrados",
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
            text="Los viajes aparecerán aquí una vez que el conductor realice trayectos",
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

    def create_trip_widget(self, trip):
        """
        Crea un widget para mostrar información de un viaje con texto correctamente contenido
        """
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(140),  # Aumentamos un poco la altura
            padding=dp(15),  # Reducimos padding para más espacio interno
            spacing=dp(8)
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

        # Contenedor de información de viaje
        info_container = BoxLayout(
            orientation='vertical',
            size_hint_y=0.7,  # 70% del espacio para la información
            spacing=dp(5)
        )

        # ID del viaje
        trip_id = trip.get('id', 'N/A')
        short_id = trip_id[:12] + "..." if len(trip_id) > 12 else trip_id

        id_label = Label(
            text=f"ID: {short_id}",
            font_size=sp(15),
            bold=True,
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=dp(25),
            color=self.colors['text'],
            text_size=(None, None),  # Inicialmente None
            markup=True
        )
        
        # Configurar text_size después de añadir al widget
        def setup_id_label_text_size(instance, value):
            # Dejamos margen para el padding del contenedor
            instance.text_size = (value - dp(30), None)
        
        id_label.bind(width=setup_id_label_text_size)

        # Origen
        start_location = trip.get('start_location', 'No especificado')
        # Truncar texto si es muy largo
        if len(start_location) > 35:
            start_location = start_location[:35] + "..."
            
        start_label = Label(
            text=f"Origen: {start_location}",
            font_size=sp(13),
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=dp(22),
            color=self.colors['text_secondary'],
            text_size=(None, None)
        )
        
        def setup_start_label_text_size(instance, value):
            instance.text_size = (value - dp(30), None)
        
        start_label.bind(width=setup_start_label_text_size)

        # Destino
        end_location = trip.get('end_location', 'No especificado')
        # Truncar texto si es muy largo
        if len(end_location) > 35:
            end_location = end_location[:35] + "..."
            
        end_label = Label(
            text=f"Destino: {end_location}",
            font_size=sp(13),
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=dp(22),
            color=self.colors['text_secondary'],
            text_size=(None, None)
        )
        
        def setup_end_label_text_size(instance, value):
            instance.text_size = (value - dp(30), None)
        
        end_label.bind(width=setup_end_label_text_size)

        # Añadir labels al contenedor de información
        info_container.add_widget(id_label)
        info_container.add_widget(start_label)
        info_container.add_widget(end_label)

        # Contenedor del botón
        button_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.3,  # 30% del espacio para el botón
            padding=[dp(0), dp(5), dp(0), dp(0)]
        )

        # Espaciador para centrar el botón a la derecha
        spacer = Label(size_hint_x=0.55)

        # Botón de acción
        view_reports_btn = Button(
            text="Ver Reportes",
            size_hint_x=0.45,
            size_hint_y=None,
            height=dp(32),
            font_size=sp(12),
            bold=True,
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=self.colors['text']
        )

        # Estilo personalizado para el botón
        with view_reports_btn.canvas.before:
            Color(*self.colors['primary'])
            view_reports_btn.bg_rect = RoundedRectangle(
                pos=view_reports_btn.pos,
                size=view_reports_btn.size,
                radius=[dp(16)]
            )
            Color(*self.colors['border'])
            view_reports_btn.border_line = Line(
                width=dp(1),
                rounded_rectangle=(
                    view_reports_btn.x, view_reports_btn.y, 
                    view_reports_btn.width, view_reports_btn.height, 
                    dp(16)
                )
            )

        view_reports_btn.bind(
            size=self.update_button_canvas,
            pos=self.update_button_canvas,
            on_press=lambda x: self.view_trip_reports(trip)
        )

        # Efecto hover para botón
        def on_button_press(instance):
            with instance.canvas.before:
                Color(148/255, 139/255, 125/255, 1)  # Color más oscuro
                instance.bg_rect = RoundedRectangle(
                    pos=instance.pos,
                    size=instance.size,
                    radius=[dp(16)]
                )
                Color(*self.colors['border'])
                instance.border_line = Line(
                    width=dp(1),
                    rounded_rectangle=(
                        instance.x, instance.y, 
                        instance.width, instance.height, 
                        dp(16)
                    )
                )

        def on_button_release(instance):
            with instance.canvas.before:
                Color(*self.colors['primary'])
                instance.bg_rect = RoundedRectangle(
                    pos=instance.pos,
                    size=instance.size,
                    radius=[dp(16)]
                )
                Color(*self.colors['border'])
                instance.border_line = Line(
                    width=dp(1),
                    rounded_rectangle=(
                        instance.x, instance.y, 
                        instance.width, instance.height, 
                        dp(16)
                    )
                )

        view_reports_btn.bind(on_press=on_button_press, on_release=on_button_release)

        button_container.add_widget(spacer)
        button_container.add_widget(view_reports_btn)

        # Agregar todos los elementos al contenedor principal
        container.add_widget(info_container)
        container.add_widget(button_container)

        return container

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

    def view_trip_reports(self, trip):
        """
        Navega a la pantalla de reportes del viaje seleccionado
        """
        try:
            app = App.get_running_app()

            # Guardar el trip_id seleccionado en la app
            app.selected_trip_id = trip.get('id')

            # También mantener la referencia al conductor
            app.selected_driver = self.driver_data

            print(f"Navegando a reportes del viaje: {trip.get('id')}")
            print(f"Conductor: {self.driver_data['name'] if self.driver_data else 'N/A'}")

            # Animación de salida
            Animation(opacity=0, duration=0.2).start(self)
            
            # Navegar a la pantalla de reportes
            self.manager.current = 'view_reports_admin'

        except Exception as e:
            print(f"Error al navegar a reportes del viaje: {e}")
            import traceback
            traceback.print_exc()

    def clear_trips(self):
        """
        Limpia la lista de viajes
        """
        try:
            self.ids.trips_list.clear_widgets()
        except:
            pass

    def refresh_trips(self):
        """
        Actualiza la lista de viajes
        """
        print("Actualizando lista de viajes...")
        self.ids.status_label.text = "Actualizando..."
        self.load_trips()

    def go_back(self):
        """
        Regresa a la pantalla de conductores
        """
        try:
            print("Regresando a la pantalla de conductores...")
            # Animación de salida
            Animation(opacity=0, duration=0.2).start(self)
            self.manager.current = 'dashboard_admin'
        except Exception as e:
            print(f"Error al regresar: {e}")
            import traceback
            traceback.print_exc()