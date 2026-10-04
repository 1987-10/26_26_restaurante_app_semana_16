from pathlib import Path
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

class RestauranteServicio:
    def __init__(self, archivo_servicio):
        self.archivo_servicio = archivo_servicio
        self.ruta_base = Path(__file__).resolve().parent.parent / "datos"
        self.productos = []
        self.usuarios = []
        self.ventas = []
        self.cargar_datos()

    def cargar_datos(self):
        datos_prod = self.archivo_servicio.cargar_json(self.ruta_base / "productos.json")
        self.productos = [Producto.desde_diccionario(p) for p in datos_prod]

        datos_usr = self.archivo_servicio.cargar_json(self.ruta_base / "usuarios.json")
        self.usuarios = [Usuario.desde_diccionario(u) for u in datos_usr]

        datos_ventas = self.archivo_servicio.cargar_json(self.ruta_base / "ventas.json")
        self.ventas = [Venta.desde_diccionario(v) for v in datos_ventas]

    def guardar_productos(self):
        lista_dict = [p.a_diccionario() for p in self.productos]
        self.archivo_servicio.guardar_json(self.ruta_base / "productos.json", lista_dict)

    def guardar_usuarios(self):
        lista_dict = [u.a_diccionario() for u in self.usuarios]
        self.archivo_servicio.guardar_json(self.ruta_base / "usuarios.json", lista_dict)

    def guardar_ventas(self):
        lista_dict = [v.a_diccionario() for v in self.ventas]
        self.archivo_servicio.guardar_json(self.ruta_base / "ventas.json", lista_dict)

    def validar_acceso(self, username: str, password: str):
        for usr in self.usuarios:
            if (usr.username.lower() == username.lower() or usr.correo.lower() ==username.lower()) and str(usr.password) == str(password):
                return usr
        return None

    def obtener_productos(self):
        return self.productos

    def obtener_usuarios(self):
        return self.usuarios

    def obtener_ventas(self):
        return self.ventas

    def obtener_usuario_por_id(self, id_usr: int):
        for u in self.usuarios:
            if u.id == id_usr:
                return u
        return None

    # --- CRUD PRODUCTOS ---
    def agregar_producto(self, id_prod: int, nombre: str, precio: float, categoria: str):
        for p in self.productos:
            if p.id == id_prod:
                return False, "El ID del producto ya existe."
        nuevo = Producto(id_prod, nombre, precio, categoria)
        self.productos.append(nuevo)
        self.guardar_productos()
        return True, "Producto registrado correctamente."

    def actualizar_producto(self, id_prod: int, nombre: str, precio: float, categoria: str):
        for p in self.productos:
            if p.id == id_prod:
                p.nombre = nombre
                p.precio = precio
                p.categoria = categoria
                self.guardar_productos()
                return True, "Producto actualizado correctamente."
        return False, "Producto no encontrado."

    def eliminar_producto(self, id_prod: int):
        for p in self.productos:
            if p.id == id_prod:
                self.productos.remove(p)
                self.guardar_productos()
                return True, "Producto eliminado correctamente."
        return False, "Producto no encontrado."

    # --- CRUD USUARIOS (SEMANA 16) ---
    def agregar_usuario(self, id_usr: int, nombre: str, username: str, correo: str, cedula: str, password: str, rol: str):
        for u in self.usuarios:
            if u.id == id_usr:
                return False, "El ID del usuario ya existe."
            if u.username.lower() == username.lower():
                return False, "El nombre de usuario ya está registrado."
            if u.cedula == cedula and cedula.strip() != "":
                return False, "La cédula ya se encuentra registrada."

        nuevo = Usuario(id_usr, nombre, username, correo, cedula, password, rol)
        self.usuarios.append(nuevo)
        self.guardar_usuarios()
        return True, "Usuario registrado correctamente."

    def actualizar_usuario(self, id_usr: int, nombre: str, username: str, correo: str, cedula: str, password: str, rol: str):
        for u in self.usuarios:
            if u.id == id_usr:
                u.nombre = nombre
                u.username = username
                u.correo = correo
                u.cedula = cedula
                if password.strip():
                    u.password = password
                u.rol = rol
                self.guardar_usuarios()
                return True, "Usuario actualizado correctamente."
        return False, "Usuario no encontrado."

    def eliminar_usuario(self, id_usr: int):
        for u in self.usuarios:
            if u.id == id_usr:
                self.usuarios.remove(u)
                self.guardar_usuarios()
                return True, "Usuario eliminado correctamente."
        return False, "Usuario no encontrado."

    # --- VENTAS ---
    def registrar_venta(self, usuario_nom: str, producto_nom: str):
        if not usuario_nom or not producto_nom:
            return False, "Debe seleccionar un usuario y un producto válidos."
        
        nuevo_id = f"V-{len(self.ventas) + 1:03d}"
        nueva_venta = Venta(nuevo_id, usuario_nom, producto_nom)
        self.ventas.append(nueva_venta)
        self.guardar_ventas()
        return True, f"Venta {nuevo_id} registrada con éxito."