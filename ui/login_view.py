import os
import tkinter as tk
from tkinter import messagebox

try:
    from PIL import Image, ImageTk
    PIL_DISPONIBLE = True
except ImportError:
    PIL_DISPONIBLE = False

class LoginView(tk.Frame):
    def __init__(self, parent, restaurante_servicio, on_login_success):
        super().__init__(parent, bg="#f5f7fa")
        self.restaurante_servicio = restaurante_servicio
        self.on_login_success = on_login_success

        self.crear_widgets()

    def obtener_ruta_logo(self):
        # Busca directamente en la carpeta assets/logo/logo.png
        dir_ui = os.path.dirname(os.path.abspath(__file__))
        dir_app = os.path.dirname(dir_ui)
        
        posibles = [
            os.path.join(dir_app, "assets", "logo", "logo1.png"),
            os.path.join(dir_app, "assets", "logo1.png"),
            os.path.join(os.getcwd(), "assets", "logo", "logo1.png"),
            os.path.join(os.getcwd(), "restaurante_app1", "assets", "logo", "logo1.png")
        ]
        for p in posibles:
            if os.path.exists(p):
                return p
        return None

    def crear_widgets(self):
        frame_login = tk.LabelFrame(
            self, text=" 🔐 Inicio de Sesión ", font=("Segoe UI", 11, "bold"),
            bg="#ffffff", fg="#2c3e50", padx=25, pady=25, bd=1, relief="solid"
        )
        frame_login.place(relx=0.5, rely=0.5, anchor="center")

        ruta_logo = self.obtener_ruta_logo()
        self.img_logo = None

        if ruta_logo:
            try:
                if PIL_DISPONIBLE:
                    pil_img = Image.open(ruta_logo)
                    pil_img = pil_img.resize((100, 100), Image.Resampling.LANCZOS)
                    self.img_logo = ImageTk.PhotoImage(pil_img)
                else:
                    self.img_logo = tk.PhotoImage(file=ruta_logo)
                    if self.img_logo.width() > 100:
                        sub = int(self.img_logo.width() / 100)
                        if sub > 1:
                            self.img_logo = self.img_logo.subsample(sub)

                lbl_logo = tk.Label(frame_login, image=self.img_logo, bg="#ffffff")
                lbl_logo.image = self.img_logo
                lbl_logo.grid(row=0, column=0, columnspan=2, pady=(0, 15))
            except Exception as e:
                print(f"Error cargando imagen de login: {e}")

        offset = 1 if self.img_logo is not None else 0

        tk.Label(frame_login, text="Usuario:", bg="#ffffff", font=("Segoe UI", 10, "bold")).grid(row=offset, column=0, sticky="e", padx=5, pady=8)
        self.txt_user = tk.Entry(frame_login, width=22, font=("Segoe UI", 10), bd=1, relief="solid")
        self.txt_user.grid(row=offset, column=1, padx=5, pady=8)

        tk.Label(frame_login, text="Contraseña:", bg="#ffffff", font=("Segoe UI", 10, "bold")).grid(row=offset+1, column=0, sticky="e", padx=5, pady=8)
        self.txt_pass = tk.Entry(frame_login, width=22, font=("Segoe UI", 10), show="*", bd=1, relief="solid")
        self.txt_pass.grid(row=offset+1, column=1, padx=5, pady=8)

        btn_ingresar = tk.Button(
            frame_login, text="Ingresar", command=self.validar_login,
            font=("Segoe UI", 10, "bold"), bg="#27ae60", fg="white",
            activebackground="#219653", activeforeground="white", bd=0, relief="flat", padx=15, pady=6, cursor="hand2"
        )
        btn_ingresar.grid(row=offset+2, column=0, columnspan=2, pady=(15, 5))

        self.txt_user.bind("<Return>", lambda e: self.validar_login())
        self.txt_pass.bind("<Return>", lambda e: self.validar_login())

    def validar_login(self):
        usr = self.txt_user.get().strip()
        pwd = self.txt_pass.get().strip()

        if not usr or not pwd:
            messagebox.showwarning("Atención", "Ingrese usuario y contraseña.")
            return

        usuario_obj = self.restaurante_servicio.validar_acceso(usr, pwd)
        if usuario_obj:
            self.on_login_success(usuario_obj)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")