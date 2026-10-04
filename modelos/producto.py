class Producto:
    def __init__(self, id: int, nombre: str, precio: float, categoria: str, codigo_unico: str = None):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.codigo_unico = codigo_unico if codigo_unico else f"PROD-{id:03d}"

    def a_diccionario(self):
        return {
            "id": self.id,
            "codigo_unico": self.codigo_unico,
            "nombre": self.nombre,
            "precio": self.precio,
            "categoria": self.categoria
        }

    @staticmethod
    def desde_diccionario(datos):
        return Producto(
            id=datos.get("id"),
            nombre=datos.get("nombre", ""),
            precio=datos.get("precio", 0.0),
            categoria=datos.get("categoria", ""),
            codigo_unico=datos.get("codigo_unico")
        )