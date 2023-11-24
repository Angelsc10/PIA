import re
import pickle
import os

# Clase Acciones que contiene metodos para registrar, eliminar, actualizar y ver informacion de asistentes
class Acciones:
    def __init__(self, generales):
        self.generales = generales

    # Metodo para agregar un nuevo asistente
    def registrar_asistente(self):
        print("\n**** REGISTRAR ASISTENTE ****")
        matricula = input("Matricula: ")

        if matricula in self.generales.asistentes:
            print("Error: Asistente con esta matrícula ya registrado.")
            return

        nombre = input("Nombre(s): ")
        apellido1 = input("apellido paterno: ")
        apellido2 = input("apellido:materno ")
        fecha_nacimiento = input("Fecha de nacimiento (DD/MM/AAAA): ")

        print("Carreras:")
        for key in sorted(self.generales.carreras.keys()):
            print(f'[{key}] {self.generales.carreras[key]}')
        carrera = self.generales.elegir_letra("Selecciona la carrera: ", self.generales.carreras.keys())

        self.generales.asistentes[matricula] = {
            'nombre': nombre,
            'apellido1': apellido1,
            'apellido2': apellido2,
            'fecha_nacimiento': fecha_nacimiento,
            'carrera': self.generales.carreras[carrera],
            'eventos_asistidos': []
        }

        print(f'\nAsistente {nombre} {apellido1} registrado exitosamente.\n')

    # Metodo para eliminar un asistente
    def eliminar_asistente(self):
        print("\n--ELIMINAR ASISTENTE--")
        matricula = input("Matricula del asistente: ")

        if matricula in self.generales.asistentes:
            del self.generales.asistentes[matricula]
            print(f'\nAsistente con matricula {matricula} eliminado exitosamente.')
        else:
            print("Error: Asistente no registrado.")

    # Metodo para actualizar la informacion de un asistente
    def actualizar_asistente(self):
        print("\n**** ACTUALIZACION DEL ASISTENTE ****")
        matricula = input("Matrícula del asistente a actualizar: ")
        if matricula in self.generales.asistentes:
            asistente = self.generales.asistentes[matricula]
            print("Datos actuales del asistente:")
            print(f'1. Nombre: {asistente["nombre"]}')
            print(f'2. Primer apellido: {asistente["apellido1"]}')
            print(f'3. Segundo apellido: {asistente["apellido2"]}')
            print(f'4. Fecha de nacimiento: {asistente["fecha_nacimiento"]}')
            print(f'5. Carrera: {asistente["carrera"]}')

            opcion = input("Selecciona el número del dato que deseas actualizar (o 'X' para salir): ")
            if opcion.isdigit() and 1 <= int(opcion) <= 5:
                opcion = int(opcion)
                nuevo_valor = input(f"Ingrese el nuevo valor para {'Nombre' if opcion == 1 else 'Primer apellido' if opcion == 2 else 'Segundo apellido' if opcion == 3 else 'Fecha de nacimiento' if opcion == 4 else 'Carrera'}: ")

                if opcion == 1:
                    asistente["nombre"] = nuevo_valor
                elif opcion == 2:
                    asistente["apellido1"] = nuevo_valor
                elif opcion == 3:
                    asistente["apellido2"] = nuevo_valor
                elif opcion == 4:
                    asistente["fecha_nacimiento"] = nuevo_valor
                elif opcion == 5:

                    print("Carreras:")
                    for key in sorted(self.generales.carreras.keys()):
                        print(f'[{key}] {self.generales.carreras[key]}')
                    carrera = self.generales.elegir_letra("Selecciona la nueva carrera: ", self.generales.carreras.keys())
                    asistente["carrera"] = self.generales.carreras[carrera]

                    print("Asistente actualizado exitosamente.")
                elif opcion.upper() == 'X':
                    print("Actualizacion cancelada.")
            else:
                print("Error: Opcion no valida.")
        else:
            print("Error: Asistente no registrado.")

    # Metodo para mostrar la informacion de un asistente
    def mostrar_info_asistente(self):
        print("\n**** INFORMACION DE ASISTENTE ****")
        matricula = input("Matricula del asistente: ")

        if matricula in self.generales.asistentes:
            asistente_info = self.generales.asistentes[matricula]
            print(f'\nMatricula: {matricula}')
            print(f'Nombre: {asistente_info["nombre"]} {asistente_info["apellido1"]} {asistente_info["apellido2"]}')
            print(f'Carrera: {asistente_info["carrera"]}')
            print(f'Fecha de nacimiento: {asistente_info["fecha_nacimiento"]}')
            print("Eventos Asistidos:")
            eventos_asistidos = asistente_info['eventos_asistidos']
            for evento_id in eventos_asistidos:
                conferencia_info = self.generales.conferencias[evento_id]
                print(f'[{evento_id}] {conferencia_info[1]} - {conferencia_info[0]} en {self.generales.auditorios[conferencia_info[3]][0]}')

            if len(eventos_asistidos) >= 3 and 'constancia' not in asistente_info:
                self.generales.asistentes[matricula]['constancia'] = True
                print("**Constancia de participacion emitida.")
                self.generales.guardar_datos()
            elif 'constancia' in asistente_info:
                print("**Constancia de participacion emitida.")
            else:
                print("**Constancia de participacion no emitida.")
        else:
            print("Error: Asistente no registrado.")

# Clase Generales que contiene datos generales y metodos relacionados
class Generales:
    def __init__(self):
        self.auditorios = {
            'A': ['Gumersindo Cantu Hinojosa', 1000],
            'B': ['Victor Gomez', 200],
            'C': ['Casas Alatriste', 150]
        }

        self.conferencias = {
            1: ['04/11/2023 15:00', 'Inteligencia Artificial en los Negocios', 'Dr. Alvaro Francisco Salazar', 'A', 0, ''],
            2: ['05/11/2023 09:00', 'Uso de la nube para gestion de procesos', 'Dr. Manuel Leos', 'B', 0, ''],
            3: ['05/11/2023 14:00', 'Industria 4.0 retos y oportunidades', 'Dra. Monica Hernandez', 'C', 0, ''],
            4: ['05/11/2023 19:00', 'Machine Learning for a better world', 'Dr. Janick Jameson', 'C', 0, ''],
            5: ['06/11/2023 15:00', 'Retos de la Banca Electronica en Mexico', 'Ing. Clara Benavides', 'A', 0, '']
        }

        self.carreras = {
            'LTI': 'LICENCIADO EN TECNOLOGIA DE LA INFORMACION',
            'LA': 'LICENCIADO EN ADMINISTRACION',
            'CP': 'CONTADOR PUBLICO',
            'LNI': 'LICENCIADO EN NEGOCIOS INTERNACIONALES',
            'LGRS': 'LICENCIADO EN GESTION DE RESPONSABILIDAD SOCIAL'
        }

        self.asistentes = {}

    # Metodo para guardar la informacion de asistentes en un archivo
    def guardar_datos(self):
        with open('asistentes.pkl', 'wb') as archivo:
            pickle.dump(self.asistentes, archivo)

    # Metodo para leer la informacion de asistentes desde un archivo
    def leer_datos(self):
        if os.path.exists('asistentes.pkl'):
            with open('asistentes.pkl', 'rb') as archivo:
                self.asistentes = pickle.load(archivo)
        else:
            self.asistentes = {}

    # Metodo para mostrar los espacios disponibles por conferencia
    def mostrar_espacios_disponibles(self):
        print("\n**** ESPACIOS DISPONIBLES POR CONFERENCIA ****")
        for key, value in self.conferencias.items():
            disponibles = self.auditorios[value[3]][1] - value[4]
            print(f'[{key}] {value[1]} - {value[0]} en {self.auditorios[value[3]][0]} ({disponibles} lugares disponibles)')

    # Metodo para mostrar eventos asistidos por un asistente
    def mostrar_eventos_asistidos(self, matricula):
        if matricula in self.asistentes:
            eventos_asistidos = self.asistentes[matricula]['eventos_asistidos']
            if eventos_asistidos:
                print("\n\EVENTOS ASISTIDOS POR EL ASISTENTE//")
                for evento_id in eventos_asistidos:
                    print(f'[{evento_id}] {self.conferencias[evento_id][1]} - {self.conferencias[evento_id][0]} en {self.auditorios[self.conferencias[evento_id][3]][0]}')
            else:
                print("El asistente no ha registrado asistencia a ningun evento.")
        else:
            print("Error: Asistente no registrado.")

    # Metodo para elegir una letra de una lista de opciones validas
    def elegir_letra(self, prompt: str, opciones_validas: str):
        while True:
            opcion = input(prompt).upper()
            if not opcion:
                print('Error en captura. Opcion no se puede omitir. Intentelo de nuevo.')
                continue
            if opcion not in opciones_validas:
                print('Error en captura. Opcion no reconocida. Intentelo de nuevo.')
                continue
            return opcion

    # Metodo para mostrar un menu y obtener la opcion seleccionada
    def mostrar_menu(self, opciones, titulo='OPCIONES DISPONIBLES'):
        print(titulo)
        opciones_validas = ''
        for k, v in opciones.items():
            print(f'[{k}] {v}')
            opciones_validas += k
        opc = self.elegir_letra('Que deseas hacer?: ', opciones_validas)
        return opc

    # Metodo para registrar la asistencia de un asistente a un evento
    def registrar_asistencia_evento(self):
        print("\n**** REGISTRAR ASISTENCIA(S) A EL EVENTO ****")
        matricula = input("Matricula del asistente: ")
        if matricula not in self.asistentes:
            print("Error: Asistente no registrado.")
            return
        eventos_asistidos = self.asistentes[matricula]['eventos_asistidos']
        if eventos_asistidos:
            print("\n \EVENTOS ASISTIDOS//")
            for evento_id in eventos_asistidos:
                print(f'[{evento_id}] {self.conferencias[evento_id][1]} - {self.conferencias[evento_id][0]} en {self.auditorios[self.conferencias[evento_id][3]][0]}')

            try:
                evento_id = int(input("Selecciona el evento por su ID para registrar asistencia: "))
            except ValueError:
                print("Error: Ingresa un valor numerico valido para el ID del evento.")
                return

            if evento_id.isdigit() and int(evento_id) in eventos_asistidos:
                evento_id = int(evento_id)
                print(f'\nAsistente {self.asistentes[matricula]["nombre"]} {self.asistentes[matricula]["apellido1"]} ha asistido al evento.')

                self.conferencias[evento_id][1] = "Asistencia confirmada"

                if len(eventos_asistidos) >= 3 and 'constancia' not in self.asistentes[matricula]:
                    self.asistentes[matricula]['constancia'] = True

            else:
                print("Error: ID de evento no valido.")
        else:
            print("Error: El asistente no ha registrado asistencia a ningun evento.")

# Clase CRUD que hereda de Acciones y Generales
class CRUD(Acciones, Generales):
    def __init__(self):
        Acciones.__init__(self, self)
        Generales.__init__(self)

    # Metodo para registrar la asistencia de un asistente a un evento
    def registrar_asistente_evento(self):
        print("\n**** REGISTRO DEL ASISTENTE(S) A EL EVENTO ****")
        matricula = input("Matricula del asistente: ")

        if matricula not in self.asistentes:
            print("Error: Asistente no registrado.")
            return

        self.mostrar_espacios_disponibles()
        evento_id = input("Selecciona el evento por su ID: ")

        if evento_id.isdigit() and int(evento_id) in self.conferencias:
            evento_id = int(evento_id)
            if evento_id not in self.asistentes[matricula]['eventos_asistidos']:
                disponibles = self.auditorios[self.conferencias[evento_id][3]][1] - self.conferencias[evento_id][4]
                if disponibles > 0:
                    self.asistentes[matricula]['eventos_asistidos'].append(evento_id)
                    self.conferencias[evento_id][4] += 1
                    print(f'\nAsistente {self.asistentes[matricula]["nombre"]} {self.asistentes[matricula]["apellido1"]} registrado para el evento.')
                else:
                    print("Error: No hay lugares disponibles para este evento.")
            else:
                print("Error: El asistente ya esta registrado para este evento.")
        else:
            print("Error: ID de evento no valido.")

# Funcion principal que ejecuta el programa
def main():
      # Crear una instancia de la clase CRUD
    crud = CRUD()
        # Leer datos almacenados previamente
    crud.leer_datos()

    # Definir opciones del menu principal
    opciones_menu_principal = {
        'A': 'Registrar asistente',
        'B': 'Eliminar asistente',
        'C': 'Actualizar asistente',
        'D': 'Ver informacion de asistente',
        'E': 'registrar asistente a evento',
        'F': 'Ver espacios disponibles por conferencia',
        'G': 'Ver eventos asistidos por un asistente',
        'X': 'Salir\n'
    }

    while True:
        # Mostrar el menu principal y obtener la opcion seleccionada
        opcion_elegida = crud.mostrar_menu(opciones_menu_principal, '\n \\MENÚ PRINCIPAL//\n')
        # Realizar acciones segun la opcion seleccionada
        if opcion_elegida == 'A':
            crud.registrar_asistente()
            crud.guardar_datos()

        elif opcion_elegida == 'B':
            crud.eliminar_asistente()
            crud.guardar_datos()

        elif opcion_elegida == 'C':
            crud.actualizar_asistente()
            crud.guardar_datos()

        elif opcion_elegida == 'D':
            crud.mostrar_info_asistente()

        elif opcion_elegida == 'E':
            crud.registrar_asistente_evento()
            crud.guardar_datos()

        elif opcion_elegida == 'F':
            crud.mostrar_espacios_disponibles()

        elif opcion_elegida == 'G':
            matricula = input("Matricula del asistente: ")
            crud.mostrar_eventos_asistidos(matricula)

        elif opcion_elegida == 'X':
            print('Gracias por usar este sistema.')
            crud.guardar_datos()
            break

        else:
            print('Opcion no disponible.')

# Si este script se ejecuta directamente, llama a la funcion principal
if __name__ == "__main__":
    main()
    print("Esperamos que disfrute del evento que escogio.")
