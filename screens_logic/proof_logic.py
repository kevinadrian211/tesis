from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.clock import Clock  # Necesario para programar la ejecución posterior
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Leer las credenciales desde las variables de entorno
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Crear el cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class ProofScreen(Screen):
    def on_enter(self):  # Se ejecuta cuando la pantalla se muestra
        # Usamos Clock.schedule_once para asegurarnos de que los ids estén disponibles
        Clock.schedule_once(self.setup_trips_box, 0)

    def setup_trips_box(self, dt):  # dt es el delta time
        # Ahora podemos acceder a trips_box, ya que se ejecuta después de que la pantalla haya cargado
        self.trips_box = self.ids.trips_box

    def load_data(self):
        """
        Función que carga los datos de los viajes desde la base de datos y los muestra en la pantalla.
        """
        try:
            # Obtenemos los datos de los viajes desde Supabase
            trips = supabase.table('trips').select('*').execute()

            # Limpiamos los widgets previos
            self.trips_box.clear_widgets()

            # Si hay datos de viajes, los mostramos en la pantalla
            if trips.data:
                for trip in trips.data:
                    trip_label = Label(
                        text=f"Trip ID: {trip['id']}\nDriver ID: {trip['driver_id']}\nStart Time: {trip['start_time']}\n"
                    )
                    self.trips_box.add_widget(trip_label)
            else:
                # Si no hay viajes, mostrar un mensaje
                self.trips_box.add_widget(Label(text="No hay viajes disponibles."))

        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            # Mostrar mensaje de error en la interfaz si la conexión falla
            self.trips_box.clear_widgets()
            self.trips_box.add_widget(Label(text=f"Error al cargar los datos: {e}"))
