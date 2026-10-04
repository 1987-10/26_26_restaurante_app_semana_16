import tkinter as tk
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RESTAURANTE - Tkinter")
        self.geometry("900x650")
        self.config(bg="#f5f7fa")

        # Inicialización de servicios
        self.archivo_servicio = ArchivoServicio()
        self.restaurante_servicio = RestauranteServicio(self.archivo_servicio)

        self.vista_actual = None
        self.mostrar_login()

    def mostrar_login(self):
        if self.vista_actual:
            self.vista_actual.destroy()

        self.vista_actual = LoginView(
            parent=self,
            restaurante_servicio=self.restaurante_servicio,
            on_login_success=lambda usuario: self.mostrar_main_view(usuario)
        )
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_main_view(self, usuario_autenticado):
        if self.vista_actual:
            self.vista_actual.destroy()

        self.vista_actual = MainView(
            parent=self,
            restaurante_servicio=self.restaurante_servicio,
            usuario_actual=usuario_autenticado,
            on_logout=self.mostrar_login
        )
        self.vista_actual.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()