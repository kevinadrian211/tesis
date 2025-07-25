from kivy.uix.screenmanager import Screen

class TypeAccountScreen(Screen):
    def select_account_type(self, account_type):
        """
        Función que maneja la selección del tipo de cuenta.
        Aquí redirigimos a la pantalla de registro.
        """
        print(f"Tipo de cuenta seleccionado: {account_type}")
        
        # Pasar account_type a la pantalla de registro
        register_screen = self.manager.get_screen('register')
        register_screen.account_type = account_type  # Asignar el tipo de cuenta a la propiedad
        self.manager.current = 'register'  # Redirigir a la pantalla de registro
