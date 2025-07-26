from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.metrics import dp

class TypeAccountScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.colors = {
            'background': (255/255, 252/255, 242/255, 1),
            'surface': (204/255, 197/255, 185/255, 1),
            'primary': (168/255, 159/255, 145/255, 1),
            'border': (20/255, 26/255, 28/255, 1),
            'text': (20/255, 26/255, 28/255, 1),
            'text_secondary': (20/255, 26/255, 28/255, 0.7)
        }

    def on_enter(self):
        self.opacity = 0
        Animation(opacity=1, duration=0.3).start(self)


    def select_account_type(self, account_type):
        print(f"Tipo de cuenta seleccionado: {account_type}")
        register_screen = self.manager.get_screen('register')
        register_screen.account_type = account_type
        self.manager.current = 'register'
