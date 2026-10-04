from datetime import datetime

class Venta:
    def __init__(self, id_venta: str, usuario: str, producto: str, fecha: str = None, codigo_unico: str = None):
        self.id_venta = id_venta
        self.usuario = usuario
        self.producto = producto
        self.fecha = fecha if fecha else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.codigo_unico = codigo_unico if codigo_unico else f"VEN-{id_venta.replace('V-', '')}"

    def a_diccionario(self):
        return {
            "id_venta": self.id_venta,
            "codigo_unico": self.codigo_unico,
            "usuario": self.usuario,
            "producto": self.producto,
            "fecha": self.fecha
        }

    @staticmethod
    def desde_diccionario(datos):
        return Venta(
            id_venta=datos.get("id_venta"),
            usuario=datos.get("usuario", ""),
            producto=datos.get("producto", ""),
            fecha=datos.get("fecha"),
            codigo_unico=datos.get("codigo_unico")
        )