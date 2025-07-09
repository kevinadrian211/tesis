from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from database import register_company, register_driver, get_all_companies

class RegisterScreen(Screen):
    account_type = StringProperty("")  # Usamos StringProperty para hacer la propiedad reactiva
    company_name = StringProperty("")  # Para el nombre de la compañía
    driver_name = StringProperty("")   # Para el nombre del conductor
    driver_email = StringProperty("")  # Para el correo electrónico del conductor
    driver_password = StringProperty("")  # Para la contraseña del conductor
    company_email = StringProperty("")  # Correo de la compañía
    company_password = StringProperty("")  # Contraseña de la compañía
    company_id = StringProperty("")  # ID de la compañía, solo necesario para conductores

    def on_enter(self):
        """
        Este método se ejecuta cuando se entra en la pantalla de registro.
        Aquí, configuramos los campos a mostrar según el tipo de cuenta.
        """
        print(f"Llegaste como: {self.account_type}")
        
        # Si llegamos como company, se deben mostrar los campos correspondientes a company
        if self.account_type == "company":
            self.clear_fields_for_driver()  # Limpiamos cualquier campo de driver si es una company
            print("Campos de Company visibles.")
        elif self.account_type == "driver":
            self.clear_fields_for_company()  # Limpiamos cualquier campo de company si es un driver
            print("Campos de Driver visibles.")
        
    def clear_fields_for_company(self):
        """Limpiar campos que no son necesarios para Company"""
        self.ids.driver_name_input.text = ""
        self.ids.driver_email_input.text = ""
        self.ids.driver_password_input.text = ""
        self.ids.company_email_input.text = ""  # Limpiar campo de correo de la compañía
        self.ids.company_password_input.text = ""  # Limpiar campo de contraseña de la compañía

    def clear_fields_for_driver(self):
        """Limpiar campos que no son necesarios para Driver"""
        self.ids.company_name_input.text = ""
        self.ids.company_email_input.text = ""  # Limpiar campo de correo de la compañía
        self.ids.company_password_input.text = ""  # Limpiar campo de contraseña de la compañía

    def go_back(self):
        """
        Esta función maneja la navegación hacia la pantalla anterior (Login).
        Cambia la pantalla activa de ScreenManager a 'login'.
        """
        self.manager.current = 'login'  # Ahora redirige directamente al login

    def register_action(self):
        """
        Este método se ejecuta cuando se hace clic en el botón "Registrar".
        Dependiendo del tipo de cuenta, realiza la validación de los campos.
        """
        print("Botón 'Registrar' presionado.")
        
        try:
            # Validamos si los campos necesarios están completos
            if self.account_type == "company":
                # Validamos si los campos necesarios están llenos
                if not self.ids.company_name_input.text or not self.ids.company_email_input.text or not self.ids.company_password_input.text:
                    print("Error: Todos los campos son obligatorios.")
                    return
                
                # Capturamos los datos de los campos
                name = self.ids.company_name_input.text.strip()
                email = self.ids.company_email_input.text.strip()
                password = self.ids.company_password_input.text.strip()

                # Llamamos a la función de registro de la base de datos
                company_id = register_company(name, email, password)
                if company_id:
                    print(f"Compañía '{name}' registrada correctamente.")
                    # Redirigimos a la pantalla de dashboard_company
                    self.manager.current = 'dashboard_company'  # Aquí redirigimos a la pantalla de la compañía
                else:
                    print("Hubo un problema al registrar la compañía.")
            
            elif self.account_type == "driver":
                # Validamos que todos los campos de driver estén completos
                if not self.ids.driver_name_input.text or not self.ids.driver_email_input.text or not self.ids.driver_password_input.text:
                    print("Error: Todos los campos son obligatorios.")
                    return
                
                # Verificamos que el ID de la compañía no sea vacío
                if not self.company_id:
                    print("Error: No se encontró el ID de la compañía.")
                    return
                
                # Capturamos los datos del conductor
                name = self.ids.driver_name_input.text.strip()
                email = self.ids.driver_email_input.text.strip()
                password = self.ids.driver_password_input.text.strip()

                # Llamamos a la función de registro de la base de datos para el conductor
                if register_driver(name, email, password, self.company_id):
                    print("Conductor registrado correctamente.")
                    # Redirigimos a la pantalla de init_report (solo conductores pueden acceder)
                    self.manager.current = 'init_report'  # Redirige a la pantalla de reporte inicial
                else:
                    print("Hubo un problema al registrar el conductor.")
        
        except Exception as e:
            print(f"Ocurrió un error inesperado durante el registro: {e}")
        
    def get_company_list(self):
        """
        Obtiene una lista de las compañías registradas.
        Esta función es llamada desde el archivo .kv
        """
        try:
            companies = get_all_companies()  # Obtenemos todas las compañías de la base de datos
            print(f"Compañías obtenidas de la base de datos: {companies}")  # Imprime las compañías obtenidas
            return [company['name'] for company in companies]  # Retorna solo los nombres de las compañías
        except Exception as e:
            print(f"Error al obtener la lista de compañías: {e}")
            return []


    def on_company_selected(self, company_name):
        """
        Este método maneja la selección de una compañía desde el Spinner.
        Captura el ID de la compañía seleccionada.
        """
        try:
            companies = get_all_companies()  # Obtenemos todas las compañías
            print(f"Compañías disponibles: {companies}")  # Imprime las compañías disponibles

            for company in companies:
                print(f"Buscando compañía con nombre: {company['name']}")  # Imprime el nombre de cada compañía
                if company['name'] == company_name:  # Si el nombre coincide
                    self.company_id = company['id']  # Asignamos el ID de la compañía
                    print(f"Compañía seleccionada: {company_name} con ID {self.company_id}")
                    break
        except Exception as e:
            print(f"Error al seleccionar la compañía: {e}")
