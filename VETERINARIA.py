from datetime import datetime


class Usuario:
    def __init__(self, nombre: str, telefono: str, direccion: str):
        self.__nombre = nombre
        self.__telefono = telefono
        self.__direccion = direccion

    def get_nombre(self): return self.__nombre
    def set_nombre(self, nombre): self.__nombre = nombre

    def get_telefono(self): return self.__telefono
    def set_telefono(self, telefono): self.__telefono = telefono

    def get_direccion(self): return self.__direccion
    def set_direccion(self, direccion): self.__direccion = direccion

    def __str__(self):
        return f"{self.__nombre} - Tel: {self.__telefono} - Dir: {self.__direccion}"


class Mascota:
    def __init__(self, nombre: str, especie: str, raza: str, edad: int):
        self.__nombre = nombre
        self.__especie = especie
        self.__raza = raza
        if edad < 0:
            raise ValueError("La edad no puede ser negativa")
        self.__edad = edad

    def get_nombre(self): return self.__nombre
    def set_nombre(self, nombre): self.__nombre = nombre

    def get_especie(self): return self.__especie
    def set_especie(self, especie): self.__especie = especie

    def get_raza(self): return self.__raza
    def set_raza(self, raza): self.__raza = raza

    def get_edad(self): return self.__edad
    def set_edad(self, edad):
        if edad < 0:
            raise ValueError("La edad no puede ser negativa")
        self.__edad = edad

    def __str__(self):
        return f"{self.__nombre} ({self.__especie} - {self.__raza}) Edad: {self.__edad}"


class Cliente(Usuario):
    def __init__(self, nombre: str, telefono: str, direccion: str):
        super().__init__(nombre, telefono, direccion)
        self.__mascotas = []

    def agregar_mascota(self, mascota: Mascota):
        if not isinstance(mascota, Mascota):
            raise TypeError("Se debe pasar un objeto Mascota")
        self.__mascotas.append(mascota)

    def eliminar_mascota_por_indice(self, idx: int):
        if idx < 0 or idx >= len(self.__mascotas):
            raise IndexError("Índice inválido")
        del self.__mascotas[idx]

    def get_mascotas(self):
        return list(self.__mascotas)

    def __str__(self):
        return super().__str__()


class Veterinario(Usuario):
    def __init__(self, nombre: str, telefono: str, direccion: str, especialidad: str, disponible: bool = True):
        super().__init__(nombre, telefono, direccion)
        self.__especialidad = especialidad
        self.__disponible = disponible

    def get_especialidad(self): return self.__especialidad
    def set_especialidad(self, esp): self.__especialidad = esp

    def get_disponible(self): return self.__disponible
    def set_disponible(self, disp: bool): self.__disponible = bool(disp)

    def __str__(self):
        return f"{self.get_nombre()} - {self.__especialidad} - Disponible: {self.__disponible}"


class Producto:
    def __init__(self, nombre: str, precio: float, stock: int):
        self.__nombre = nombre
        if precio < 0:
            raise ValueError("Precio inválido")
        self.__precio = precio
        if stock < 0:
            raise ValueError("Stock inválido")
        self.__stock = stock

    def get_nombre(self): return self.__nombre
    def set_nombre(self, nombre): self.__nombre = nombre

    def get_precio(self): return self.__precio
    def set_precio(self, precio):
        if precio < 0: raise ValueError("Precio inválido")
        self.__precio = precio

    def get_stock(self): return self.__stock
    def set_stock(self, stock):
        if stock < 0: raise ValueError("Stock inválido")
        self.__stock = stock

    def reducir_stock(self, cantidad: int):
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser positiva")
        if cantidad > self.__stock:
            raise ValueError("Stock insuficiente")
        self.__stock -= cantidad

    def aumentar_stock(self, cantidad: int):
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser positiva")
        self.__stock += cantidad

    def __str__(self):
        return f"{self.__nombre} - ${self.__precio:.2f} - Stock: {self.__stock}"


class Turno:
    def __init__(self, mascota: Mascota, cliente: Cliente, veterinario: Veterinario, fecha_hora: datetime):
        if not isinstance(fecha_hora, datetime):
            raise ValueError("fecha_hora debe ser objeto datetime")
        self.__mascota = mascota
        self.__cliente = cliente
        self.__veterinario = veterinario
        self.__fecha_hora = fecha_hora

    def get_mascota(self): return self.__mascota
    def get_cliente(self): return self.__cliente
    def get_veterinario(self): return self.__veterinario
    def get_fecha_hora(self): return self.__fecha_hora

    def set_fecha_hora(self, fecha_hora: datetime):
        if not isinstance(fecha_hora, datetime):
            raise ValueError("fecha_hora debe ser objeto datetime")
        self.__fecha_hora = fecha_hora

    def __str__(self):
        f = self.__fecha_hora.strftime("%d/%m/%Y %H:%M")
        return f"Turno: {self.__cliente.get_nombre()} - {self.__mascota.get_nombre()} con {self.__veterinario.get_nombre()} el {f}"


class Venta:
    def __init__(self, cliente: Cliente, producto: Producto, cantidad: int):
        if not isinstance(cliente, Cliente):
            raise TypeError("cliente debe ser Cliente")
        if not isinstance(producto, Producto):
            raise TypeError("producto debe ser Producto")
        if cantidad <= 0:
            raise ValueError("cantidad debe ser positiva")
        producto.reducir_stock(cantidad)
        self.__cliente = cliente
        self.__producto = producto
        self.__cantidad = cantidad
        self.__total = producto.get_precio() * cantidad
        self.__fecha_hora = datetime.now()

    def get_cliente(self): return self.__cliente
    def get_producto(self): return self.__producto
    def get_cantidad(self): return self.__cantidad
    def get_total(self): return self.__total
    def get_fecha_hora(self): return self.__fecha_hora

    def __str__(self):
        f = self.__fecha_hora.strftime("%d/%m/%Y %H:%M")
        return f"Venta: {self.__cliente.get_nombre()} - {self.__producto.get_nombre()} x{self.__cantidad} - Total: ${self.__total:.2f} ({f})"


clientes = []
veterinarios = []
productos = []
turnos = []
ventas = []


def buscar_cliente_por_nombre(nombre: str):
    for c in clientes:
        if c.get_nombre().lower() == nombre.lower():
            return c
    return None


def buscar_veterinario_por_nombre(nombre: str):
    for v in veterinarios:
        if v.get_nombre().lower() == nombre.lower():
            return v
    return None


def buscar_producto_por_nombre(nombre: str):
    for p in productos:
        if p.get_nombre().lower() == nombre.lower():
            return p
    return None


def seleccionar_mascota_de_cliente(cliente: Cliente):
    mascotas = cliente.get_mascotas()
    if not mascotas:
        return None
    if len(mascotas) == 1:
        return mascotas[0]

    print("El cliente tiene varias mascotas. Elegí por número:")
    for i, m in enumerate(mascotas):
        print(f"{i + 1}. {m}")
    while True:
        try:
            sel = int(input("Número de mascota: "))
            if 1 <= sel <= len(mascotas):
                return mascotas[sel - 1]
            else:
                print("Número fuera de rango.")
        except ValueError:
            print("Ingresa un número válido.")


def leer_fecha(input_text="Fecha y hora (dd/mm/yyyy HH:MM): "):
    while True:
        txt = input(input_text)
        try:
            return datetime.strptime(txt, "%d/%m/%Y %H:%M")
        except ValueError:
            print("Formato inválido. Usa dd/mm/yyyy HH:MM (por ejemplo: 25/12/2025 14:30).")


def menu_principal():
    while True:
        print("SISTEMA VETERINARIA")
        print("1  - Registrar cliente")
        print("2  - Agregar mascota a cliente")
        print("3  - Listar clientes y mascotas")
        print("4  - Registrar veterinario")
        print("5  - Listar veterinarios")
        print("6  - Registrar turno")
        print("7  - Listar turnos")
        print("8  - Registrar producto")
        print("9  - Listar productos")
        print("10 - Registrar venta")
        print("11 - Listar ventas")
        print("12 - Eliminar cliente")
        print("13 - Eliminar mascota de cliente")
        print("14 - Salir")
        op = input("Opción: ").strip()

        if op == "1":
            nombre = input("Nombre: ").strip()
            telefono = input("Teléfono: ").strip()
            direccion = input("Dirección: ").strip()
            clientes.append(Cliente(nombre, telefono, direccion))
            print("Cliente registrado.")

        elif op == "2":
            nombre_cliente = input("Nombre del cliente: ").strip()
            cliente = buscar_cliente_por_nombre(nombre_cliente)
            if not cliente:
                print("Cliente no encontrado.")
                continue
            nombre_m = input("Nombre mascota: ").strip()
            especie = input("Especie: ").strip()
            raza = input("Raza: ").strip()
            try:
                edad = int(input("Edad (años): ").strip())
            except ValueError:
                print("Edad inválida. Debe ser número entero.")
                continue
            try:
                mascota = Mascota(nombre_m, especie, raza, edad)
                cliente.agregar_mascota(mascota)
                print("Mascota agregada al cliente.")
            except Exception as e:
                print("Error:", e)

        elif op == "3":
            if not clientes:
                print("No hay clientes registrados.")
            for c in clientes:
                print(f"- {c.get_nombre()} | Tel: {c.get_telefono()} | Dir: {c.get_direccion()}")
                mascotas = c.get_mascotas()
                if not mascotas:
                    print("   (Sin mascotas)")
                else:
                    for m in mascotas:
                        print("   -", m)

        elif op == "4":
            nombre = input("Nombre: ").strip()
            telefono = input("Teléfono: ").strip()
            direccion = input("Dirección: ").strip()
            especialidad = input("Especialidad: ").strip()
            veterinarios.append(Veterinario(nombre, telefono, direccion, especialidad))
            print("Veterinario registrado.")

        elif op == "5":
            if not veterinarios:
                print("No hay veterinarios registrados.")
            for v in veterinarios:
                print("-", v)

        elif op == "6":
            nombre_cliente = input("Nombre del cliente: ").strip()
            cliente = buscar_cliente_por_nombre(nombre_cliente)
            if not cliente:
                print("Cliente no encontrado.")
                continue
            mascota = seleccionar_mascota_de_cliente(cliente)
            if not mascota:
                print("El cliente no tiene mascotas.")
                continue
            nombre_vet = input("Nombre del veterinario: ").strip()
            vet = buscar_veterinario_por_nombre(nombre_vet)
            if not vet:
                print("Veterinario no encontrado.")
                continue
            fecha = leer_fecha()
            try:
                turno = Turno(mascota, cliente, vet, fecha)
                turnos.append(turno)
                print("Turno registrado:", turno)
            except Exception as e:
                print("Error al registrar turno:", e)

        elif op == "7":
            if not turnos:
                print("No hay turnos registrados.")
            for t in turnos:
                print("-", t)

        elif op == "8":
            nombre = input("Nombre producto: ").strip()
            try:
                precio = float(input("Precio: ").strip())
                stock = int(input("Stock inicial: ").strip())
            except ValueError:
                print("Precio o stock inválido.")
                continue
            try:
                productos.append(Producto(nombre, precio, stock))
                print("Producto registrado.")
            except Exception as e:
                print("Error:", e)

        elif op == "9":
            if not productos:
                print("No hay productos registrados.")
            for p in productos:
                print("-", p)

        elif op == "10":
            nombre_cliente = input("Nombre del cliente: ").strip()
            cliente = buscar_cliente_por_nombre(nombre_cliente)
            if not cliente:
                print("Cliente no encontrado.")
                continue
            nombre_producto = input("Nombre del producto: ").strip()
            producto = buscar_producto_por_nombre(nombre_producto)
            if not producto:
                print("Producto no encontrado.")
                continue
            try:
                cantidad = int(input("Cantidad: ").strip())
            except ValueError:
                print("Cantidad inválida.")
                continue
            try:
                venta = Venta(cliente, producto, cantidad)
                ventas.append(venta)
                print("Venta registrada:", venta)
            except Exception as e:
                print("Error al registrar venta:", e)

        elif op == "11":
            if not ventas:
                print("No hay ventas registradas.")
            for v in ventas:
                print("-", v)

        elif op == "12":
            nombre_cliente = input("Nombre del cliente a eliminar: ").strip()
            cliente = buscar_cliente_por_nombre(nombre_cliente)
            if not cliente:
                print("Cliente no encontrado.")
                continue
            clientes.remove(cliente)
            print("Cliente eliminado.")

        elif op == "13":
            nombre_cliente = input("Nombre del cliente: ").strip()
            cliente = buscar_cliente_por_nombre(nombre_cliente)
            if not cliente:
                print("Cliente no encontrado.")
                continue
            mascotas = cliente.get_mascotas()
            if not mascotas:
                print("El cliente no tiene mascotas.")
                continue
            for i, m in enumerate(mascotas):
                print(f"{i + 1}. {m}")
            try:
                idx = int(input("Número de mascota a eliminar: ")) - 1
                cliente.eliminar_mascota_por_indice(idx)
                print("Mascota eliminada.")
            except Exception as e:
                print("Error:", e)

        elif op == "14":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu_principal()
