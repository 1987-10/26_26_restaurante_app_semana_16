import json

class ArchivoServicio:
    @staticmethod
    def cargar_json(ruta_archivo):
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except Exception as e:
            print(f"Error al leer {ruta_archivo}: {e}")
            return []

    @staticmethod
    def guardar_json(ruta_archivo, datos):
        try:
            with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al escribir {ruta_archivo}: {e}")
            return False