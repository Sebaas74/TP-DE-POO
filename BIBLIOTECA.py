class Libro:
    def __init__(self, titulo, autor, codigo):
        self.__titulo = titulo
        self.__autor = autor
        self.__codigo = codigo
        self.__disponible = True
        self.__prestado_a = None

    def get_titulo(self):
        return self.__titulo

    def set_titulo(self, titulo):
        self.__titulo = titulo

    def get_autor(self):
        return self.__autor

    def set_autor(self, autor):
        self.__autor = autor

    def get_codigo(self):
        return self.__codigo

    def set_codigo(self, codigo):
        self.__codigo = codigo

    def get_disponible(self):
        return self.__disponible

    def set_disponible(self, estado):
        self.__disponible = estado

    def get_prestado_a(self):
        return self.__prestado_a

    def set_prestado_a(self, persona):
        self.__prestado_a = persona


class Persona:
    def __init__(self, nombre, identificador):
        self.__nombre = nombre
        self.__identificador = identificador
        self.__libros_en_prestamo = []

    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        self.__nombre = nombre

    def get_identificador(self):
        return self.__identificador

    def set_identificador(self, identificador):
        self.__identificador = identificador

    def get_libros_en_prestamo(self):
        return self.__libros_en_prestamo

    def pedir_libro(self, libro):
        if libro.get_disponible():
            libro.set_disponible(False)
            libro.set_prestado_a(self)
            self.__libros_en_prestamo.append(libro)
            return True
        return False

    def devolver_libro(self, libro):
        if libro in self.__libros_en_prestamo:
            libro.set_disponible(True)
            libro.set_prestado_a(None)
            self.__libros_en_prestamo.remove(libro)
            return True
        return False


class Biblioteca:
    def __init__(self):
        self.__lista_libros = []
        self.__lista_personas = []


    def agregar_libro(self, libro):
        self.__lista_libros.append(libro)

    def get_lista_libros(self):
        return self.__lista_libros


    def agregar_persona(self, persona):
        self.__lista_personas.append(persona)

    def get_lista_personas(self):
        return self.__lista_personas


    def mostrar_libros(self):
        for libro in self.__lista_libros:
            estado = "Disponible" if libro.get_disponible() else f"Prestado a {libro.get_prestado_a().get_nombre()}"
            print(f"{libro.get_titulo()} - {estado}")

    def mostrar_personas(self):
        for persona in self.__lista_personas:
            libros = [libro.get_titulo() for libro in persona.get_libros_en_prestamo()]
            print(f"{persona.get_nombre()} ({persona.get_identificador()}): {libros if libros else 'Sin libros'}")

def menu():
    biblioteca = Biblioteca()

    while True:
        print("MENÚ BIBLIOTECA")
        print("1. Agregar libro")
        print("2. Agregar persona")
        print("3. Prestar libro")
        print("4. Devolver libro")
        print("5. Mostrar estado de los libros")
        print("6. Mostrar estado de las personas")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            titulo = input("Título del libro: ")
            autor = input("Autor del libro: ")
            codigo = input("Código del libro: ")
            libro = Libro(titulo, autor, codigo)
            biblioteca.agregar_libro(libro)
            print("Libro agregado correctamente.")

        elif opcion == "2":
            nombre = input("Nombre de la persona: ")
            identificador = input("Identificador de la persona: ")
            persona = Persona(nombre, identificador)
            biblioteca.agregar_persona(persona)
            print("Persona agregada correctamente.")

        elif opcion == "3":
            if not biblioteca.get_lista_libros() or not biblioteca.get_lista_personas():
                print("Primero debe agregar libros y personas.")
                continue

            print("\n--- Libros disponibles ---")
            disponibles = [libro for libro in biblioteca.get_lista_libros() if libro.get_disponible()]
            for i, libro in enumerate(disponibles):
                print(f"{i}. {libro.get_titulo()} ({libro.get_autor()})")

            if not disponibles:
                print("No hay libros disponibles.")
                continue

            libro_idx = int(input("Seleccione el número del libro a prestar: "))

            print("\n--- Personas ---")
            for j, persona in enumerate(biblioteca.get_lista_personas()):
                print(f"{j}. {persona.get_nombre()} (ID: {persona.get_identificador()})")

            persona_idx = int(input("Seleccione el número de la persona: "))

            if biblioteca.get_lista_personas()[persona_idx].pedir_libro(disponibles[libro_idx]):
                print("Libro prestado correctamente.")
            else:
                print("El libro no está disponible.")

        elif opcion == "4":
            print("\n--- Personas ---")
            for j, persona in enumerate(biblioteca.get_lista_personas()):
                print(f"{j}. {persona.get_nombre()} (ID: {persona.get_identificador()})")

            persona_idx = int(input("Seleccione el número de la persona: "))
            persona = biblioteca.get_lista_personas()[persona_idx]

            if not persona.get_libros_en_prestamo():
                print("Esta persona no tiene libros en préstamo.")
                continue

            print("\n--- Libros en préstamo de esta persona ---")
            for i, libro in enumerate(persona.get_libros_en_prestamo()):
                print(f"{i}. {libro.get_titulo()} ({libro.get_autor()})")

            libro_idx = int(input("Seleccione el número del libro a devolver: "))

            if persona.devolver_libro(persona.get_libros_en_prestamo()[libro_idx]):
                print("Libro devuelto correctamente.")
            else:
                print("Error al devolver el libro.")

        elif opcion == "5":
            print("\n--- Estado de los libros ---")
            biblioteca.mostrar_libros()

        elif opcion == "6":
            print("\n--- Estado de las personas ---")
            biblioteca.mostrar_personas()

        elif opcion == "0":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida, intente de nuevo.")


if __name__ == "__main__":
    menu()

