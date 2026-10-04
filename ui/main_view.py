import os
import tkinter as tk
from tkinter import ttk, messagebox

try:
    from PIL import Image, ImageTk
    PIL_DISPONIBLE = True
except ImportError:
    PIL_DISPONIBLE = False

class MainView(tk.Frame):
    def __init__(self, parent, restaurante_servicio, usuario_actual, on_logout):
        super().__init__(parent, bg="#f5f7fa")
        self.restaurante_servicio = restaurante_servicio
        self.usuario_actual = usuario_actual
        self.on_logout = on_logout

        self.configurar_estilos()
        self.crear_widgets()

    def obtener_ruta_logo(self):
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        while directorio_actual:
            posible_logo = os.path.join(directorio_actual, "assets", "logo", "logo.png")
            if os.path.exists(posible_logo):
                return posible_logo
            padre = os.path.dirname(directorio_actual)
            if padre == directorio_actual:
                break
            directorio_actual = padre
        return None

    def configurar_estilos(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("TNotebook", background="#f5f7fa", borderwidth=0)
        self.style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[15, 6])
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", "#ffffff"), ("!selected", "#e2e8f0")],
            foreground=[("selected", "#2c3e50"), ("!selected", "#64748b")]
        )

        self.style.configure("Productos.Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#2c3e50", foreground="white")
        self.style.configure("Ventas.Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#1e8449", foreground="white")
        self.style.configure("Usuarios.Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#8e44ad", foreground="white")

    def crear_boton_dinamico(self, parent, text, command, bg_color, hover_color, fg_color="white"):
        btn = tk.Button(
            parent, text=text, command=command, font=("Segoe UI", 9, "bold"),
            bg=bg_color, fg=fg_color, activebackground=hover_color, activeforeground=fg_color,
            bd=0, relief="flat", padx=12, pady=6, cursor="hand2"
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
        return btn

    def crear_widgets(self):
        # Header
        frame_header = tk.Frame(self, bg="#ffffff", bd=1, relief="solid")
        frame_header.pack(fill="x", padx=15, pady=(10, 5))

        # Cargador de la imagen del logo en el Header
        ruta_logo = self.obtener_ruta_logo()
        self.img_logo_header = None

        if ruta_logo:
            try:
                if PIL_DISPONIBLE:
                    pil_img = Image.open(ruta_logo)
                    pil_img = pil_img.resize((32, 32), Image.Resampling.LANCZOS)
                    self.img_logo_header = ImageTk.PhotoImage(pil_img)
                else:
                    self.img_logo_header = tk.PhotoImage(file=ruta_logo)
                    if self.img_logo_header.width() > 32:
                        sub = int(self.img_logo_header.width() / 32)
                        if sub > 1:
                            self.img_logo_header = self.img_logo_header.subsample(sub)

                lbl_logo = tk.Label(frame_header, image=self.img_logo_header, bg="#ffffff")
                lbl_logo.image = self.img_logo_header
                lbl_logo.pack(side="left", padx=(10, 0), pady=5)
            except Exception as e:
                print(f"Error al cargar logo en header: {e}")

        # Obtención dinámica del nombre del usuario autenticado
        user_name = getattr(self.usuario_actual, 'nombre', '') or getattr(self.usuario_actual, 'username', 'Usuario')
        user_rol = getattr(self.usuario_actual, 'rol', 'Empleado')

        lbl_titulo = tk.Label(
            frame_header,
            text=f"RESTAURANTE — Usuario: {user_name} ({user_rol})",
            font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#2c3e50", padx=10, pady=8
        )
        lbl_titulo.pack(side="left")

        btn_salir = self.crear_boton_dinamico(frame_header, "🚪 Cerrar Sesión", self.on_logout, "#e74c3c", "#c0392b")
        btn_salir.pack(side="right", padx=10, pady=5)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=10)

        # 📦 PESTAÑA 1: PRODUCTOS
        self.tab_productos = tk.Frame(self.notebook, bg="#ffffff")
        self.notebook.add(self.tab_productos, text=" 📦 Productos ")

        banner_p = tk.Label(self.tab_productos, text="GESTIÓN DE PRODUCTOS", font=("Segoe UI", 9, "bold"), bg="#ebf5fb", fg="#2980b9", pady=6)
        banner_p.pack(fill="x")

        frame_form_p = tk.LabelFrame(self.tab_productos, text=" Datos del Producto ", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg="#2c3e50", padx=10, pady=10)
        frame_form_p.pack(fill="x", padx=15, pady=8)

        tk.Label(frame_form_p, text="ID:", bg="#ffffff", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="e", padx=5, pady=4)
        self.txt_id = tk.Entry(frame_form_p, width=10, font=("Segoe UI", 9), bd=1, relief="solid")
        self.txt_id.grid(row=0, column=1, sticky="w", padx=5, pady=4)

        tk.Label(frame_form_p, text="Nombre:", bg="#ffffff", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="e", padx=5, pady=4)
        self.txt_nombre = tk.Entry(frame_form_p, width=22, font=("Segoe UI", 9), bd=1, relief="solid")
        self.txt_nombre.grid(row=0, column=3, sticky="w", padx=5, pady=4)

        tk.Label(frame_form_p, text="Precio ($):", bg="#ffffff", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="e", padx=5, pady=4)
        self.txt_precio = tk.Entry(frame_form_p, width=10, font=("Segoe UI", 9), bd=1, relief="solid")
        self.txt_precio.grid(row=1, column=1, sticky="w", padx=5, pady=4)

        tk.Label(frame_form_p, text="Categoría:", bg="#ffffff", font=("Segoe UI", 9, "bold")).grid(row=1, column=2, sticky="e", padx=5, pady=4)
        self.txt_categoria = tk.Entry(frame_form_p, width=22, font=("Segoe UI", 9), bd=1, relief="solid")
        self.txt_categoria.grid(row=1, column=3, sticky="w", padx=5, pady=4)

        frame_acciones_p = tk.Frame(self.tab_productos, bg="#ffffff")
        frame_acciones_p.pack(fill="x", padx=15, pady=5)

        self.crear_boton_dinamico(frame_acciones_p, "➕ Registrar", self.guardar_producto, "#27ae60", "#219653").pack(side="left", padx=3)
        self.crear_boton_dinamico(frame_acciones_p, "📋 Cargar Formulario", self.cargar_en_formulario, "#f39c12", "#d68910").pack(side="left", padx=3)
        self.crear_boton_dinamico(frame_acciones_p, "✏️️ Actualizar", self.modificar_producto, "#2980b9", "#1f618d").pack(side="left", padx=3)
        self.crear_boton_dinamico(frame_acciones_p, "🗑️ Eliminar", self.borrar_producto, "#c0392b", "#962d22").pack(side="left", padx=3)
        self.crear_boton_dinamico(frame_acciones_p, "🧹 Limpiar", self.limpiar_formulario, "#7f8c8d", "#616a6b").pack(side="left", padx=3)

        frame_tabla_p = tk.Frame(self.tab_productos, bg="#ffffff")
        frame_tabla_p.pack(fill="both", expand=True, padx=15, pady=(5, 10))

        cols_p = ("ID", "Código", "Nombre", "Precio", "Categoría")
        self.tree_productos = ttk.Treeview(frame_tabla_p, columns=cols_p, show="headings", style="Productos.Treeview")
        for col in cols_p:
            self.tree_productos.heading(col, text=col)
            self.tree_productos.column(col, anchor="center", width=100)

        scroll_p = ttk.Scrollbar(frame_tabla_p, orient="vertical", command=self.tree_productos.yview)
        self.tree_productos.configure(yscroll=scroll_p.set)
        self.tree_productos.pack(side="left", fill="both", expand=True)
        scroll_p.pack(side="right", fill="y")

        # 🛒 PESTAÑA 2: VENTAS
        self.tab_ventas = tk.Frame(self.notebook, bg="#ffffff")
        self.notebook.add(self.tab_ventas, text=" 🛒 Ventas ")

        banner_v = tk.Label(self.tab_ventas, text="REGISTRO Y CONSULTA DE VENTAS", font=("Segoe UI", 9, "bold"), bg="#e8f8f5", fg="#1e8449", pady=6)
        banner_v.pack(fill="x")

        frame_form_v = tk.LabelFrame(self.tab_ventas, text=" Registrar Operación ", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg="#1e8449", padx=10, pady=10)
        frame_form_v.pack(fill="x", padx=15, pady=8)

        tk.Label(frame_form_v, text="Usuario / Atiende:", bg="#ffffff", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.cb_usuarios = ttk.Combobox(frame_form_v, state="readonly", width=20, font=("Segoe UI", 9))
        self.cb_usuarios.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        tk.Label(frame_form_v, text="Producto a Vender:", bg="#ffffff", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.cb_productos = ttk.Combobox(frame_form_v, state="readonly", width=25, font=("Segoe UI", 9))
        self.cb_productos.grid(row=0, column=3, sticky="w", padx=5, pady=5)

        btn_vender = self.crear_boton_dinamico(frame_form_v, "🛒 Confirmar Venta", self.callback_registrar_venta, "#27ae60", "#1e8449")
        btn_vender.grid(row=0, column=4, padx=15, pady=5)

        frame_tabla_v = tk.Frame(self.tab_ventas, bg="#ffffff")
        frame_tabla_v.pack(fill="both", expand=True, padx=15, pady=(5, 10))

        cols_v = ("ID Venta", "Código Único", "Usuario", "Producto", "Fecha y Hora")
        self.tree_ventas = ttk.Treeview(frame_tabla_v, columns=cols_v, show="headings", style="Ventas.Treeview")
        for col in cols_v:
            self.tree_ventas.heading(col, text=col)
            self.tree_ventas.column(col, anchor="center", width=120)

        scroll_v = ttk.Scrollbar(frame_tabla_v, orient="vertical", command=self.tree_ventas.yview)
        self.tree_ventas.configure(yscroll=scroll_v.set)
        self.tree_ventas.pack(side="left", fill="both", expand=True)
        scroll_v.pack(side="right", fill="y")

        # 👥 PESTAÑA 3: GESTIÓN DE USUARIOS (SOLO ADMINISTRADOR)
        if user_rol == "Administrador":
            self.tab_usuarios = tk.Frame(self.notebook, bg="#ffffff")
            self.notebook.add(self.tab_usuarios, text=" 👥 Usuarios ")

            banner_u = tk.Label(self.tab_usuarios, text="GESTIÓN DE USUARIOS — ACCESO ADMINISTRATIVO", font=("Segoe UI", 9, "bold"), bg="#f4ecf7", fg="#8e44ad", pady=6)
            banner_u.pack(fill="x")

            frame_form_u = tk.LabelFrame(self.tab_usuarios, text=" Formulario de Usuario ", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg="#8e44ad", padx=10, pady=10)
            frame_form_u.pack(fill="x", padx=15, pady=8)

            tk.Label(frame_form_u, text="ID:", bg="#ffffff", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="e", padx=5, pady=4)
            self.txt_u_id = tk.Entry(frame_form_u, width=8, font=("Segoe UI", 9), bd=1, relief="solid")
            self.txt_u_id.grid(row=0, column=1, sticky="w", padx=5, pady=4)

            tk.Label(frame_form_u, text="Nombre Completo:", bg="#ffffff", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="e", padx=5, pady=4)
            self.txt_u_nombre = tk.Entry(frame_form_u, width=18, font=("Segoe UI", 9), bd=1, relief="solid")
            self.txt_u_nombre.grid(row=0, column=3, sticky="w", padx=5, pady=4)

            tk.Label(frame_form_u, text="Username:", bg="#ffffff", font=("Segoe UI", 9, "bold")).grid(row=0, column=4, sticky="e", padx=5, pady=4)
            self.txt_u_username = tk.Entry(frame_form_u, width=14, font=("Segoe UI", 9), bd=1, relief="solid")
            self.txt_u_username.grid(row=0, column=5, sticky="w", padx=5, pady=4)

            tk.Label(frame_form_u, text="Correo:", bg="#ffffff", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="e", padx=5, pady=4)
            self.txt_u_correo = tk.Entry(frame_form_u, width=18, font=("Segoe UI", 9), bd=1, relief="solid")
            self.txt_u_correo.grid(row=1, column=1, columnspan=2, sticky="w", padx=5, pady=4)

            tk.Label(frame_form_u, text="Cédula:", bg="#ffffff", font=("Segoe UI", 9, "bold")).grid(row=1, column=3, sticky="e", padx=5, pady=4)
            self.txt_u_cedula = tk.Entry(frame_form_u, width=12, font=("Segoe UI", 9), bd=1, relief="solid")
            self.txt_u_cedula.grid(row=1, column=4, sticky="w", padx=5, pady=4)

            tk.Label(frame_form_u, text="Contraseña:", bg="#ffffff", font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="e", padx=5, pady=4)
            self.txt_u_pass = tk.Entry(frame_form_u, width=10, font=("Segoe UI", 9), show="*", bd=1, relief="solid")
            self.txt_u_pass.grid(row=2, column=1, sticky="w", padx=5, pady=4)

            tk.Label(frame_form_u, text="Rol:", bg="#ffffff", font=("Segoe UI", 9, "bold")).grid(row=2, column=2, sticky="e", padx=5, pady=4)
            self.cb_u_rol = ttk.Combobox(frame_form_u, values=["Administrador", "Empleado", "Cliente"], state="readonly", width=14, font=("Segoe UI", 9))
            self.cb_u_rol.grid(row=2, column=3, sticky="w", padx=5, pady=4)
            self.cb_u_rol.current(1)

            frame_acciones_u = tk.Frame(self.tab_usuarios, bg="#ffffff")
            frame_acciones_u.pack(fill="x", padx=15, pady=5)

            self.crear_boton_dinamico(frame_acciones_u, "➕ Registrar", self.guardar_usuario, "#27ae60", "#219653").pack(side="left", padx=3)
            self.crear_boton_dinamico(frame_acciones_u, "✏️ Actualizar", self.actualizar_usuario, "#2980b9", "#1f618d").pack(side="left", padx=3)
            self.crear_boton_dinamico(frame_acciones_u, "🗑️ Eliminar", self.eliminar_usuario, "#c0392b", "#962d22").pack(side="left", padx=3)
            self.crear_boton_dinamico(frame_acciones_u, "🧹 Limpiar (Esc)", self.limpiar_form_usuario, "#7f8c8d", "#616a6b").pack(side="left", padx=3)

            frame_tabla_u = tk.Frame(self.tab_usuarios, bg="#ffffff")
            frame_tabla_u.pack(fill="both", expand=True, padx=15, pady=(5, 10))

            cols_u = ("ID", "Código Único", "Nombre", "Username", "Correo", "Cédula", "Rol")
            self.tree_usuarios = ttk.Treeview(frame_tabla_u, columns=cols_u, show="headings", style="Usuarios.Treeview")
            for col in cols_u:
                self.tree_usuarios.heading(col, text=col)
                self.tree_usuarios.column(col, anchor="center", width=100)

            scroll_u = ttk.Scrollbar(frame_tabla_u, orient="vertical", command=self.tree_usuarios.yview)
            self.tree_usuarios.configure(yscroll=scroll_u.set)
            self.tree_usuarios.pack(side="left", fill="both", expand=True)
            scroll_u.pack(side="right", fill="y")

            # --- BINDING DE EVENTOS ---
            self.tree_usuarios.bind("<<TreeviewSelect>>", self.on_usuario_select)
            self.txt_u_id.bind("<Return>", lambda e: self.guardar_usuario())
            self.txt_u_username.bind("<Return>", lambda e: self.guardar_usuario())
            self.txt_u_pass.bind("<Return>", lambda e: self.guardar_usuario())
            self.cb_u_rol.bind("<<ComboboxSelected>>", self.on_rol_changed)
            self.bind_all("<Escape>", lambda e: self.limpiar_form_usuario())

            self.cargar_tabla_usuarios()

        self.actualizar_comboboxes()
        self.cargar_tabla_productos()
        self.cargar_tabla_ventas()

    def on_usuario_select(self, event):
        selected = self.tree_usuarios.selection()
        if selected:
            item = self.tree_usuarios.item(selected[0])
            user_id = item["values"][0]
            usuario_obj = self.restaurante_servicio.obtener_usuario_por_id(user_id)
            if usuario_obj:
                self.txt_u_id.delete(0, tk.END)
                self.txt_u_id.insert(0, str(usuario_obj.id))
                self.txt_u_nombre.delete(0, tk.END)
                self.txt_u_nombre.insert(0, getattr(usuario_obj, 'nombre', ''))
                self.txt_u_username.delete(0, tk.END)
                self.txt_u_username.insert(0, getattr(usuario_obj, 'username', ''))
                self.txt_u_correo.delete(0, tk.END)
                self.txt_u_correo.insert(0, getattr(usuario_obj, 'correo', ''))
                self.txt_u_cedula.delete(0, tk.END)
                self.txt_u_cedula.insert(0, getattr(usuario_obj, 'cedula', ''))
                self.txt_u_pass.delete(0, tk.END)
                self.txt_u_pass.insert(0, getattr(usuario_obj, 'password', ''))
                self.cb_u_rol.set(getattr(usuario_obj, 'rol', 'Empleado'))

    def on_rol_changed(self, event):
        print(f"Rol seleccionado en Combobox: {self.cb_u_rol.get()}")

    def limpiar_form_usuario(self):
        if hasattr(self, 'txt_u_id'):
            self.txt_u_id.delete(0, tk.END)
            self.txt_u_nombre.delete(0, tk.END)
            self.txt_u_username.delete(0, tk.END)
            self.txt_u_correo.delete(0, tk.END)
            self.txt_u_cedula.delete(0, tk.END)
            self.txt_u_pass.delete(0, tk.END)
            self.cb_u_rol.current(1)
            selected = self.tree_usuarios.selection()
            if selected:
                self.tree_usuarios.selection_remove(selected[0])

    def cargar_tabla_usuarios(self):
        if hasattr(self, 'tree_usuarios'):
            for item in self.tree_usuarios.get_children():
                self.tree_usuarios.delete(item)
            for u in self.restaurante_servicio.obtener_usuarios():
                nom = getattr(u, 'nombre', '')
                usr = getattr(u, 'username', '')
                cor = getattr(u, 'correo', '')
                ced = getattr(u, 'cedula', '')
                rol = getattr(u, 'rol', 'Empleado')
                cod = getattr(u, 'codigo_unico', f"USR-{u.id:03d}")
                self.tree_usuarios.insert("", "end", values=(u.id, cod, nom, usr, cor, ced, rol))

    def guardar_usuario(self):
        try:
            id_u = int(self.txt_u_id.get().strip())
            nom = self.txt_u_nombre.get().strip()
            usr = self.txt_u_username.get().strip()
            cor = self.txt_u_correo.get().strip()
            ced = self.txt_u_cedula.get().strip()
            pwd = self.txt_u_pass.get().strip()
            rol = self.cb_u_rol.get()

            if not usr or not pwd:
                messagebox.showwarning("Atención", "Username y contraseña son obligatorios.")
                return

            exito, msj = self.restaurante_servicio.agregar_usuario(id_u, nom, usr, cor, ced, pwd, rol)
            if exito:
                messagebox.showinfo("Éxito", msj)
                self.limpiar_form_usuario()
                self.cargar_tabla_usuarios()
                self.actualizar_comboboxes()
            else:
                messagebox.showerror("Error", msj)
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero.")

    def actualizar_usuario(self):
        try:
            id_u = int(self.txt_u_id.get().strip())
            nom = self.txt_u_nombre.get().strip()
            usr = self.txt_u_username.get().strip()
            cor = self.txt_u_correo.get().strip()
            ced = self.txt_u_cedula.get().strip()
            pwd = self.txt_u_pass.get().strip()
            rol = self.cb_u_rol.get()

            exito, msj = self.restaurante_servicio.actualizar_usuario(id_u, nom, usr, cor, ced, pwd, rol)
            if exito:
                messagebox.showinfo("Éxito", msj)
                self.limpiar_form_usuario()
                self.cargar_tabla_usuarios()
                self.actualizar_comboboxes()
            else:
                messagebox.showerror("Error", msj)
        except ValueError:
            messagebox.showerror("Error", "Ingrese un ID válido para actualizar.")

    def eliminar_usuario(self):
        id_text = self.txt_u_id.get().strip()
        if not id_text:
            messagebox.showwarning("Atención", "Ingrese el ID a eliminar.")
            return
        try:
            id_u = int(id_text)
            if messagebox.askyesno("Confirmar", f"¿Eliminar usuario ID {id_u}?"):
                exito, msj = self.restaurante_servicio.eliminar_usuario(id_u)
                if exito:
                    messagebox.showinfo("Éxito", msj)
                    self.limpiar_form_usuario()
                    self.cargar_tabla_usuarios()
                    self.actualizar_comboboxes()
                else:
                    messagebox.showerror("Error", msj)
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser entero.")

    # --- LÓGICA PRODUCTOS Y VENTAS ---
    def limpiar_formulario(self):
        self.txt_id.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_precio.delete(0, tk.END)
        self.txt_categoria.delete(0, tk.END)

    def cargar_tabla_productos(self):
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        for p in self.restaurante_servicio.obtener_productos():
            cod = getattr(p, 'codigo_unico', f"PROD-{p.id:03d}")
            self.tree_productos.insert("", "end", values=(p.id, cod, p.nombre, f"${p.precio:.2f}", p.categoria))

    def guardar_producto(self):
        try:
            id_p = int(self.txt_id.get().strip())
            nom = self.txt_nombre.get().strip()
            prec = float(self.txt_precio.get().strip())
            cat = self.txt_categoria.get().strip()

            if not nom or not cat:
                messagebox.showwarning("Atención", "Campos obligatorios vacíos.")
                return

            exito, msj = self.restaurante_servicio.agregar_producto(id_p, nom, prec, cat)
            if exito:
                messagebox.showinfo("Éxito", msj)
                self.limpiar_formulario()
                self.cargar_tabla_productos()
                self.actualizar_comboboxes()
            else:
                messagebox.showerror("Error", msj)
        except ValueError:
            messagebox.showerror("Error", "ID entero y precio numérico requeridos.")

    def cargar_en_formulario(self):
        id_texto = self.txt_id.get().strip()
        if not id_texto:
            messagebox.showwarning("Atención", "Ingrese el ID.")
            return
        try:
            id_buscar = int(id_texto)
            productos = self.restaurante_servicio.obtener_productos()
            encontrado = next((p for p in productos if p.id == id_buscar), None)
            if encontrado:
                self.txt_nombre.delete(0, tk.END)
                self.txt_nombre.insert(0, encontrado.nombre)
                self.txt_precio.delete(0, tk.END)
                self.txt_precio.insert(0, str(encontrado.precio))
                self.txt_categoria.delete(0, tk.END)
                self.txt_categoria.insert(0, encontrado.categoria)
                messagebox.showinfo("Cargado", "Datos cargados.")
            else:
                messagebox.showerror("Error", "Producto no encontrado.")
        except ValueError:
            messagebox.showerror("Error", "ID entero requerido.")

    def modificar_producto(self):
        try:
            id_p = int(self.txt_id.get().strip())
            nom = self.txt_nombre.get().strip()
            prec = float(self.txt_precio.get().strip())
            cat = self.txt_categoria.get().strip()

            exito, msj = self.restaurante_servicio.actualizar_producto(id_p, nom, prec, cat)
            if exito:
                messagebox.showinfo("Éxito", msj)
                self.limpiar_formulario()
                self.cargar_tabla_productos()
                self.actualizar_comboboxes()
            else:
                messagebox.showerror("Error", msj)
        except ValueError:
            messagebox.showerror("Error", "Asegúrese de ingresar un ID entero.")

    def borrar_producto(self):
        id_texto = self.txt_id.get().strip()
        if not id_texto:
            messagebox.showwarning("Atención", "Ingrese el ID.")
            return
        try:
            id_p = int(id_texto)
            if messagebox.askyesno("Confirmar", f"¿Eliminar producto ID {id_p}?"):
                exito, msj = self.restaurante_servicio.eliminar_producto(id_p)
                if exito:
                    messagebox.showinfo("Éxito", msj)
                    self.limpiar_formulario()
                    self.cargar_tabla_productos()
                    self.actualizar_comboboxes()
                else:
                    messagebox.showerror("Error", msj)
        except ValueError:
            messagebox.showerror("Error", "ID entero requerido.")

    def actualizar_comboboxes(self):
        users = self.restaurante_servicio.obtener_usuarios()
        prods = self.restaurante_servicio.obtener_productos()

        self.cb_usuarios['values'] = [getattr(u, 'nombre', '') or getattr(u, 'username', '') for u in users]
        if users:
            self.cb_usuarios.current(0)

        self.cb_productos['values'] = [p.nombre for p in prods]
        if prods:
            self.cb_productos.current(0)

    def callback_registrar_venta(self):
        usr_sel = self.cb_usuarios.get()
        prod_sel = self.cb_productos.get()

        exito, msj = self.restaurante_servicio.registrar_venta(usr_sel, prod_sel)
        if exito:
            messagebox.showinfo("Venta Exitosa", msj)
            self.cargar_tabla_ventas()
        else:
            messagebox.showerror("Error de Venta", msj)

    def cargar_tabla_ventas(self):
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)
        for v in self.restaurante_servicio.obtener_ventas():
            cod = getattr(v, 'codigo_unico', f"VEN-{v.id_venta}")
            self.tree_ventas.insert("", "end", values=(v.id_venta, cod, v.usuario, v.producto, v.fecha))