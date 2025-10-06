# sistema_facultad_completo.py
import time
class Curso:
    def __init__(self, nombre, codigo, profesor, capacidad):
        self.__nombre = nombre
        self.__codigo = codigo
        self.__profesor = profesor
        self.__capacidad = int(capacidad)
        self.__estudiantes_inscriptos = []

    # --- Getters / Setters ---
    def get_nombre(self): return self.__nombre
    def set_nombre(self, valor): self.__nombre = valor

    def get_codigo(self): return self.__codigo
    def set_codigo(self, valor): self.__codigo = valor

    def get_profesor(self): return self.__profesor
    def set_profesor(self, valor): self.__profesor = valor

    def get_capacidad(self): return self.__capacidad
    def set_capacidad(self, valor): self.__capacidad = int(valor)

    # Properties
    nombre = property(get_nombre, set_nombre)
    codigo = property(get_codigo, set_codigo)
    profesor = property(get_profesor, set_profesor)
    capacidad = property(get_capacidad, set_capacidad)

    # --- Operaciones ---
    def cupos_disponibles(self):
        return self.__capacidad - len(self.__estudiantes_inscriptos)

    def agregar_estudiante(self, estudiante):
        if estudiante in self.__estudiantes_inscriptos: 
            return False
        if self.cupos_disponibles() <= 0: 
            return False
        self.__estudiantes_inscriptos.append(estudiante)
        return True

    def baja_estudiante(self, estudiante):
        if estudiante in self.__estudiantes_inscriptos:
            self.__estudiantes_inscriptos.remove(estudiante)
            return True
        return False

    def listado_estudiantes(self):
        return list(self.__estudiantes_inscriptos)

    def __str__(self):
        return (f"Código: {self.__codigo} - Nombre: {self.__nombre} - Profesor: {self.__profesor} - "
                f"Inscritos: {len(self.__estudiantes_inscriptos)} - Cupos disponibles: {self.cupos_disponibles()}")


class Estudiante:
    def __init__(self, nombre, apellido, matricula, carrera):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__matricula = str(matricula)
        self.__carrera = carrera
        self.__cursos = []

    # --- Getters / Setters ---
    def get_nombre(self): return self.__nombre
    def set_nombre(self, valor): self.__nombre = valor

    def get_apellido(self): return self.__apellido
    def set_apellido(self, valor): self.__apellido = valor

    def get_matricula(self): return self.__matricula
    def set_matricula(self, valor): self.__matricula = str(valor)

    def get_carrera(self): return self.__carrera
    def set_carrera(self, valor): self.__carrera = valor

    def get_cursos(self): return list(self.__cursos)

    # Properties
    nombre = property(get_nombre, set_nombre)
    apellido = property(get_apellido, set_apellido)
    matricula = property(get_matricula, set_matricula)
    carrera = property(get_carrera, set_carrera)

    # --- Operaciones ---
    def inscribe_curso(self, curso):
        if curso in self.__cursos: 
            return False
        self.__cursos.append(curso)
        return True

    def baja_curso(self, curso):
        if curso in self.__cursos:
            self.__cursos.remove(curso)
            return True
        return False

    def __str__(self):
        cursos_str = ", ".join([c.get_codigo() for c in self.__cursos])
        return f"{self.__matricula} - {self.__apellido}, {self.__nombre} - {self.__carrera} | Cursos: [{cursos_str}]"


class Facultad:
    def __init__(self):
        self.__estudiantes = []
        self.__cursos = []

    # --- Gestión de estudiantes ---
    def alta_estudiante(self, nombre, apellido, matricula, carrera):
        if self.get_estudiante(matricula): 
            return False
        estudiante = Estudiante(nombre, apellido, matricula, carrera)
        self.__estudiantes.append(estudiante)
        return True

    def baja_estudiante(self, matricula):
        estudiante = self.get_estudiante(matricula)
        if not estudiante: 
            return False
        for curso in list(estudiante.get_cursos()):
            curso.baja_estudiante(estudiante)
            estudiante.baja_curso(curso)
        self.__estudiantes.remove(estudiante)
        return True

    def get_estudiante(self, matricula):
        for est in self.__estudiantes:
            if est.get_matricula() == str(matricula): 
                return est
        return None

    def listado_estudiantes(self):
        return list(self.__estudiantes)

    # --- Gestión de cursos ---
    def alta_curso(self, nombre, codigo, profesor, capacidad):
        if self.get_curso(codigo): 
            return False
        curso = Curso(nombre, codigo, profesor, capacidad)
        self.__cursos.append(curso)
        return True

    def baja_curso(self, codigo):
        curso = self.get_curso(codigo)
        if not curso: 
            return False
        for est in list(curso.listado_estudiantes()):
            curso.baja_estudiante(est)
            est.baja_curso(curso)
        self.__cursos.remove(curso)
        return True

    def get_curso(self, codigo):
        for curso in self.__cursos:
            if curso.get_codigo() == str(codigo): 
                return curso
        return None

    def listado_cursos(self):
        return list(self.__cursos)

    # --- Inscripciones ---
    def inscribe_estudiante_curso(self, matricula, codigo):
        estudiante = self.get_estudiante(matricula)
        if not estudiante: 
            return False, "Estudiante no encontrado."
        curso = self.get_curso(codigo)
        if not curso: 
            return False, "Curso no encontrado."
        if estudiante in curso.listado_estudiantes(): 
            return False, "Ya inscripto en el curso."
        if curso.cupos_disponibles() <= 0: 
            return False, "No hay cupos disponibles."
        if curso.agregar_estudiante(estudiante):
            estudiante.inscribe_curso(curso)
            return True, "Inscripción realizada correctamente."
        return False, "Error al inscribir."

    def baja_estudiante_de_curso(self, matricula, codigo):
        estudiante = self.get_estudiante(matricula)
        if not estudiante: 
            return False, "Estudiante no encontrado."
        curso = self.get_curso(codigo)
        if not curso: 
            return False, "Curso no encontrado."
        if curso.baja_estudiante(estudiante) or estudiante.baja_curso(curso):
            return True, "Baja realizada correctamente."
        return False, "El estudiante no estaba inscripto en ese curso."


# ----------------- MENÚ -----------------
def mostrar_menu():
    print("MENÚ FACULTAD")
    print("1. Alta de estudiante")
    print("2. Baja de estudiante")
    print("3. Listar estudiantes")
    print("4. Alta de curso")
    print("5. Baja de curso")
    print("6. Listar cursos")
    print("7. Inscribir estudiante en curso")
    print("8. Dar de baja estudiante de curso")
    print("9. Salir")

def ejecutar_menu():
    facultad = Facultad()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            print("\n--- Alta de Estudiante ---")
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            matricula = input("Matrícula: ")
            carrera = input("Carrera: ")
            if facultad.alta_estudiante(nombre, apellido, matricula, carrera):
                print("Estudiante agregado correctamente.")
            else:
                print("Ya existe un estudiante con esa matrícula.")
            time.sleep(2)
        elif opcion == "2":
            print("\n--- Baja de Estudiante ---")
            matricula = input("Ingrese matrícula: ")
            if facultad.baja_estudiante(matricula):
                print("Estudiante eliminado correctamente.")
            else:
                print("No se encontró estudiante con esa matrícula.")
            time.sleep(2)
        elif opcion == "3":
            print("\n--- Listado de Estudiantes ---")
            estudiantes = facultad.listado_estudiantes()
            if not estudiantes:
                print("No hay estudiantes cargados.")
            else:
                for est in estudiantes:
                    print(est)
            time.sleep(2)
        elif opcion == "4":
            print("\n--- Alta de Curso ---")
            nombre = input("Nombre del curso: ")
            codigo = input("Código del curso: ")
            profesor = input("Profesor: ")
            try:
                capacidad = int(input("Capacidad máxima: "))
            except ValueError:
                print("Capacidad inválida.")
                continue
            if facultad.alta_curso(nombre, codigo, profesor, capacidad):
                print("Curso agregado correctamente.")
            else:
                print("Ya existe un curso con ese código.")
            time.sleep(2)
        elif opcion == "5":
            print("\n--- Baja de Curso ---")
            codigo = input("Ingrese código de curso: ")
            if facultad.baja_curso(codigo):
                print("Curso eliminado correctamente.")
            else:
                print("No se encontró curso con ese código.")
            time.sleep(2)
        elif opcion == "6":
            print("\n--- Listado de Cursos ---")
            cursos = facultad.listado_cursos()
            if not cursos:
                print("No hay cursos cargados.")
            else:
                for curso in cursos:
                    print(curso)
            time.sleep(2)
        elif opcion == "7":
            print("\n--- Inscribir Estudiante en Curso ---")
            matricula = input("Matrícula: ")
            codigo = input("Código de curso: ")
            ok, msg = facultad.inscribe_estudiante_curso(matricula, codigo)
            print(msg)
            time.sleep(2)
        elif opcion == "8":
            print("\n--- Baja de Estudiante de Curso ---")
            matricula = input("Matrícula: ")
            codigo = input("Código de curso: ")
            ok, msg = facultad.baja_estudiante_de_curso(matricula, codigo)
            print(msg)
            time.sleep(2)
        elif opcion == "9":
            print("Saliendo del sistema...")
            time.sleep(2)
            break

        else:
            print("Opción inválida, intente nuevamente.")
            time.sleep(2)

# ----------------- PROGRAMA PRINCIPAL -----------------
if __name__ == "__main__":
    ejecutar_menu()
