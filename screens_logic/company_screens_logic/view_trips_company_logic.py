from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, Line, RoundedRectangle
from database import get_trips_by_driver

class ViewTripsCompanyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.driver_data = None
        self.trips_data = []

    def on_enter(self):
        """
        Se ejecuta cuando entramos a la pantalla
        """
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
                self.ids.title_label.text = f"Viajes de company {self.driver_data['name']}"
                self.ids.driver_info_label.text = f"Conductor: {self.driver_data['name']}"
                self.ids.title_label.color = (0, 0, 0, 1)  # texto negro
                self.ids.driver_info_label.color = (0, 0, 0, 1)
            else:
                print("No se encontró conductor seleccionado")
                self.ids.title_label.text = "Viajes del Conductor"
                self.ids.driver_info_label.text = "No se ha seleccionado un conductor"
                self.ids.title_label.color = (0, 0, 0, 1)
                self.ids.driver_info_label.color = (0, 0, 0, 1)

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
            self.ids.status_label.color = (0, 0, 0, 1)
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
                self.ids.status_label.color = (0, 0, 0, 1)
                no_trips_widget = self.create_no_trips_widget()
                trips_list.add_widget(no_trips_widget)
                return

            # Actualizar mensaje de estado
            self.ids.status_label.text = f"Se encontraron {len(self.trips_data)} viajes"
            self.ids.status_label.color = (0, 0, 0, 1)

            # Crear widgets para cada viaje
            for trip in self.trips_data:
                trip_widget = self.create_trip_widget(trip)
                trips_list.add_widget(trip_widget)

        except Exception as e:
            print(f"Error al actualizar lista de viajes: {e}")
            import traceback
            traceback.print_exc()
            self.ids.status_label.text = "Error al cargar viajes"
            self.ids.status_label.color = (0, 0, 0, 1)

    def create_no_trips_widget(self):
        """
        Crea un widget para mostrar cuando no hay viajes
        """
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(150),
            padding=dp(20)
        )

        # Fondo blanco
        with container.canvas.before:
            Color(1, 1, 1, 1)  # blanco
            container.rect = Rectangle(size=container.size, pos=container.pos)
            Color(0, 0, 0, 1)  # borde negro
            Line(rectangle=(container.x, container.y, container.width, container.height), width=1.2)

        container.bind(size=self.update_rect, pos=self.update_rect)

        message_label = Label(
            text="No hay viajes registrados para este conductor",
            font_size=32,
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1)
        )
        message_label.bind(size=message_label.setter('text_size'))

        container.add_widget(message_label)
        return container

    def create_trip_widget(self, trip):
        """
        Crea un widget para mostrar información de un viaje
        """
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(140),
            padding=dp(15),
            spacing=dp(8)
        )

        # Fondo blanco con borde negro y bordes redondeados
        with container.canvas.before:
            Color(1, 1, 1, 1)  # blanco
            container.rect = RoundedRectangle(radius=[dp(16)], size=container.size, pos=container.pos)
            Color(0, 0, 0, 1)  # borde negro
            container.border = Line(
                rounded_rectangle=(container.x, container.y, container.width, container.height, dp(16)),
                width=1.2
            )

        container.bind(size=self.update_rect, pos=self.update_rect)

        info_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(75),
            spacing=dp(3)
        )

        trip_id = trip.get('id', 'N/A')
        short_id = trip_id[:8] + "..." if len(trip_id) > 8 else trip_id

        id_label = Label(
            text=f"ID: {short_id}",
            font_size=32,
            bold=True,
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=dp(25),
            color=(0, 0, 0, 1)
        )
        id_label.bind(size=id_label.setter('text_size'))

        start_location = trip.get('start_location', 'No especificado')
        start_label = Label(
            text=f"Origen: {start_location}",
            font_size=32,
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=dp(25),
            color=(0, 0, 0, 1)
        )
        start_label.bind(size=start_label.setter('text_size'))

        end_location = trip.get('end_location', 'No especificado')
        end_label = Label(
            text=f"Destino: {end_location}",
            font_size=32,
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=dp(25),
            color=(0, 0, 0, 1)
        )
        end_label.bind(size=end_label.setter('text_size'))

        info_container.add_widget(id_label)
        info_container.add_widget(start_label)
        info_container.add_widget(end_label)

        button_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            padding=(dp(0), dp(5), dp(0), dp(0))
        )

        view_reports_btn = Button(
            text="Ver Reportes",
            size_hint_x=0.3,
            size_hint_y=None,
            height=dp(35),
            background_color=(1, 1, 1, 1),  # fondo blanco
            color=(0, 0, 0, 1),  # texto negro
            on_press=lambda x: self.view_trip_reports(trip)
        )

        # Borde negro para botón
        def btn_canvas(instance, value):
            instance.canvas.before.clear()
            with instance.canvas.before:
                Color(1, 1, 1, 1)
                Rectangle(pos=instance.pos, size=instance.size)
                Color(0, 0, 0, 1)
                Line(rectangle=(instance.x, instance.y, instance.width, instance.height), width=1.2)

        view_reports_btn.bind(pos=btn_canvas, size=btn_canvas)

        spacer = Label(size_hint_x=0.7)

        button_container.add_widget(spacer)
        button_container.add_widget(view_reports_btn)

        container.add_widget(info_container)
        container.add_widget(button_container)

        return container

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

            # Navegar a la pantalla de reportes
            self.manager.current = 'view_reports_company'

        except Exception as e:
            print(f"Error al navegar a reportes del viaje: {e}")
            import traceback
            traceback.print_exc()

    def update_rect(self, instance, value):
        """
        Actualiza el rectángulo y borde cuando cambia el tamaño del widget
        """
        if hasattr(instance, 'rect'):
            if isinstance(instance.rect, (Rectangle, RoundedRectangle)):
                instance.rect.pos = instance.pos
                instance.rect.size = instance.size
        if hasattr(instance, 'border'):
            if isinstance(instance.border, Line):
                instance.border.rectangle = (instance.x, instance.y, instance.width, instance.height)
                if hasattr(instance.border, 'rounded_rectangle'):
                    instance.border.rounded_rectangle = (instance.x, instance.y, instance.width, instance.height, dp(16))

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
        self.load_trips()

    def go_back(self):
        """
        Regresa a la pantalla de conductores
        """
        try:
            print("Regresando a la pantalla de conductores...")
            self.manager.current = 'view_drivers_company'
        except Exception as e:
            print(f"Error al regresar: {e}")
            import traceback
            traceback.print_exc()
