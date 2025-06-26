# root.py
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

# Cargar el archivo kv asociado
Builder.load_file("root.kv")

class RootLayout(BoxLayout):
    pass
