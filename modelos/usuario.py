class Usuario:
    def __init__(self, id: int, nombre: str, username: str, correo: str, cedula: str, password: str, rol: str = "Empleado"):
        self.id = id
        self.nombre = nombre
        self.username = username
        self.correo = correo
        self.cedula = cedula
        self.password = password
        self.rol = rol

    def a_diccionario(self):
        return {
            "id": self.id,
            "codigo_unico": f"USR-{self.cedula if self.cedula else '000'}",
            "nombre": self.nombre,
            "username": self.username,
            "correo": self.correo,
            "cedula": self.cedula,
            "password": self.password,
            "rol": self.rol
        }

    @staticmethod
    def desde_diccionario(datos):
        return Usuario(
            id=datos.get("id"),
            nombre=datos.get("nombre", ""),
            username=datos.get("username", ""),
            correo=datos.get("correo", ""),
            cedula=datos.get("cedula", ""),
            password=datos.get("password", ""),
            rol=datos.get("rol", "Empleado")
        )