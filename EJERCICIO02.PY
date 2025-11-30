import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime, date


# -------------------- MODELO --------------------

@dataclass
class Habitacion:
    numero: int
    precio_dia: int
    disponible: bool = True
    nombre: str = ""
    apellidos: str = ""
    documento: str = ""
    fecha_ingreso: Optional[date] = None


class Hotel:
    def __init__(self):
        self.habitaciones: List[Habitacion] = []
        # Habitaciones 1-5: 120000, 6-10: 160000
        for i in range(1, 11):
            precio = 120_000 if i <= 5 else 160_000
            self.habitaciones.append(Habitacion(numero=i, precio_dia=precio))

    def obtener_habitacion(self, numero: int) -> Optional[Habitacion]:
        for h in self.habitaciones:
            if h.numero == numero:
                return h
        return None


def parsear_fecha(cadena: str) -> Optional[date]:
    """
    Intenta convertir 'dd/mm/aaaa' en un objeto date.
    Devuelve None si el formato es inválido.
    """
    try:
        return datetime.strptime(cadena.strip(), "%d/%m/%Y").date()
    except ValueError:
        return None


# -------------------- APLICACIÓN TKINTER --------------------

class HotelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Hotel")
        self.geometry("600x400")

        self.hotel = Hotel()

        # Menú
        barra_menu = tk.Menu(self)
        menu_opciones = tk.Menu(barra_menu, tearoff=False)
        menu_opciones.add_command(label="Consultar habitaciones",
                                  command=self.ventana_consultar_habitaciones)
        menu_opciones.add_command(label="Salida de huéspedes",
                                  command=self.ventana_salida_huesped)
        barra_menu.add_cascade(label="Opciones", menu=menu_opciones)
        self.config(menu=barra_menu)

        lbl = tk.Label(
            self,
            text="Gestión de huéspedes del hotel\nUse el menú superior.",
            font=("Arial", 13),
            justify="center"
        )
        lbl.pack(expand=True)

    # ------------- CONSULTAR HABITACIONES / INGRESO -------------

    def ventana_consultar_habitaciones(self):
        win = tk.Toplevel(self)
        win.title("Habitaciones")
        win.geometry("500x350")
        win.grab_set()

        columnas = ("numero", "precio", "estado")
        tree = ttk.Treeview(win, columns=columnas, show="headings", height=10)
        tree.heading("numero", text="Habitación")
        tree.heading("precio", text="Precio por día")
        tree.heading("estado", text="Estado")

        tree.column("numero", width=90, anchor="center")
        tree.column("precio", width=130, anchor="e")
        tree.column("estado", width=120, anchor="center")

        for h in self.hotel.habitaciones:
            estado = "Disponible" if h.disponible else "No disponible"
            tree.insert(
                "",
                tk.END,
                values=(h.numero, f"{h.precio_dia:,}", estado)
            )

        tree.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=5)

        tk.Label(btn_frame, text="Número de habitación a ocupar:").pack(side="left")
        num_var = tk.StringVar()
        tk.Entry(btn_frame, textvariable=num_var, width=5).pack(side="left", padx=5)

        def seleccionar_habitacion():
            try:
                numero = int(num_var.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número de habitación válido.")
                return

            hab = self.hotel.obtener_habitacion(numero)
            if hab is None:
                messagebox.showerror("Error", "La habitación no existe.")
                return
            if not hab.disponible:
                messagebox.showerror("Error", "La habitación está ocupada.")
                return

            # Abrir ventana de ingreso de huésped
            self.ventana_ingreso_huesped(hab)
            win.destroy()

        tk.Button(btn_frame, text="Ocupar habitación",
                  command=seleccionar_habitacion).pack(side="left", padx=5)

    def ventana_ingreso_huesped(self, habitacion: Habitacion):
        win = tk.Toplevel(self)
        win.title(f"Ingreso huésped - Habitación {habitacion.numero}")
        win.geometry("400x300")
        win.grab_set()

        frame = tk.Frame(win, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text=f"Habitación {habitacion.numero} "
                             f"- Precio: {habitacion.precio_dia:,} por día").grid(
            row=0, column=0, columnspan=2, pady=5
        )

        # Variables
        fecha_var = tk.StringVar()
        nombre_var = tk.StringVar()
        apellidos_var = tk.StringVar()
        doc_var = tk.StringVar()

        # Campos
        tk.Label(frame, text="Fecha ingreso (dd/mm/aaaa):").grid(row=1, column=0,
                                                                 sticky="e", pady=3)
        tk.Entry(frame, textvariable=fecha_var).grid(row=1, column=1, sticky="we", pady=3)

        tk.Label(frame, text="Nombre:").grid(row=2, column=0, sticky="e", pady=3)
        tk.Entry(frame, textvariable=nombre_var).grid(row=2, column=1, sticky="we", pady=3)

        tk.Label(frame, text="Apellidos:").grid(row=3, column=0, sticky="e", pady=3)
        tk.Entry(frame, textvariable=apellidos_var).grid(row=3, column=1, sticky="we", pady=3)

        tk.Label(frame, text="Documento:").grid(row=4, column=0, sticky="e", pady=3)
        tk.Entry(frame, textvariable=doc_var).grid(row=4, column=1, sticky="we", pady=3)

        frame.columnconfigure(1, weight=1)

        def registrar_ingreso():
            fecha_str = fecha_var.get().strip()
            nombre = nombre_var.get().strip()
            apellidos = apellidos_var.get().strip()
            documento = doc_var.get().strip()

            if not fecha_str or not nombre or not apellidos or not documento:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            f_ingreso = parsear_fecha(fecha_str)
            if f_ingreso is None:
                messagebox.showerror(
                    "Error de fecha",
                    "La fecha debe tener formato dd/mm/aaaa y ser válida."
                )
                return

            # Guardar en la habitación
            habitacion.disponible = False
            habitacion.nombre = nombre
            habitacion.apellidos = apellidos
            habitacion.documento = documento
            habitacion.fecha_ingreso = f_ingreso

            messagebox.showinfo("Registro correcto",
                                "Ingreso registrado. La habitación queda no disponible.")
            win.destroy()

        btn_frame = tk.Frame(win, pady=10)
        btn_frame.pack()
        tk.Button(btn_frame, text="Registrar ingreso",
                  command=registrar_ingreso).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancelar",
                  command=win.destroy).pack(side="left", padx=5)

    # ------------- SALIDA DE HUÉSPEDES -------------

    def ventana_salida_huesped(self):
        win = tk.Toplevel(self)
        win.title("Salida de huésped")
        win.geometry("350x180")
        win.grab_set()

        frame = tk.Frame(win, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Número de habitación a entregar:").grid(
            row=0, column=0, sticky="e", pady=5
        )
        num_var = tk.StringVar()
        tk.Entry(frame, textvariable=num_var, width=6).grid(
            row=0, column=1, sticky="w", pady=5
        )

        def continuar():
            try:
                numero = int(num_var.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número de habitación válido.")
                return

            hab = self.hotel.obtener_habitacion(numero)
            if hab is None:
                messagebox.showerror("Error", "La habitación no existe.")
                return
            if hab.disponible:
                messagebox.showerror("Error", "La habitación no está ocupada.")
                return

            # Abrir ventana para registrar salida
            self.ventana_registro_salida(hab)
            win.destroy()

        btn_frame = tk.Frame(win, pady=10)
        btn_frame.pack()
        tk.Button(btn_frame, text="Continuar",
                  command=continuar).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancelar",
                  command=win.destroy).pack(side="left", padx=5)

    def ventana_registro_salida(self, habitacion: Habitacion):
        win = tk.Toplevel(self)
        win.title(f"Salida - Habitación {habitacion.numero}")
        win.geometry("420x300")
        win.grab_set()

        frame = tk.Frame(win, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        info = (
            f"Habitación {habitacion.numero} - Precio: {habitacion.precio_dia:,} por día\n"
            f"Huésped: {habitacion.nombre} {habitacion.apellidos}\n"
            f"Documento: {habitacion.documento}\n"
            f"Fecha ingreso: {habitacion.fecha_ingreso.strftime('%d/%m/%Y')}"
        )
        tk.Label(frame, text=info, justify="left").grid(
            row=0, column=0, columnspan=2, pady=5, sticky="w"
        )

        tk.Label(frame, text="Fecha salida (dd/mm/aaaa):").grid(
            row=1, column=0, sticky="e", pady=5
        )
        fecha_salida_var = tk.StringVar()
        tk.Entry(frame, textvariable=fecha_salida_var).grid(
            row=1, column=1, sticky="we", pady=5
        )

        frame.columnconfigure(1, weight=1)

        # Labels para resultado
        dias_var = tk.StringVar(value="-")
        total_var = tk.StringVar(value="-")

        tk.Label(frame, text="Días de alojamiento:").grid(
            row=2, column=0, sticky="e", pady=5
        )
        tk.Label(frame, textvariable=dias_var).grid(
            row=2, column=1, sticky="w", pady=5
        )

        tk.Label(frame, text="Total a pagar:").grid(
            row=3, column=0, sticky="e", pady=5
        )
        tk.Label(frame, textvariable=total_var).grid(
            row=3, column=1, sticky="w", pady=5
        )

        # Botones
        btn_frame = tk.Frame(win, pady=10)
        btn_frame.pack()

        btn_calcular = tk.Button(btn_frame, text="Calcular total")
        btn_registrar = tk.Button(btn_frame, text="Registrar salida")
        btn_cancelar = tk.Button(btn_frame, text="Cancelar", command=win.destroy)

        btn_calcular.pack(side="left", padx=5)
        btn_registrar.pack(side="left", padx=5)
        btn_cancelar.pack(side="left", padx=5)

        # Para cumplir con el enunciado, solo permitimos Registrar salida
        # después de una fecha válida y cálculo hecho.
        btn_registrar.config(state="disabled")

        def calcular_total():
            fecha_str = fecha_salida_var.get().strip()
            f_salida = parsear_fecha(fecha_str)
            if f_salida is None:
                messagebox.showerror(
                    "Error de fecha",
                    "La fecha debe tener formato dd/mm/aaaa y ser válida."
                )
                return

            if f_salida <= habitacion.fecha_ingreso:
                messagebox.showerror(
                    "Error de fecha",
                    "La fecha de salida debe ser mayor que la fecha de ingreso."
                )
                return

            dias = (f_salida - habitacion.fecha_ingreso).days
            total = dias * habitacion.precio_dia

            dias_var.set(str(dias))
            total_var.set(f"{total:,}")

            # Fecha válida → habilitamos registrar salida
            btn_registrar.config(state="normal")

            # Guardamos la fecha de salida temporalmente en el widget
            btn_registrar.fecha_salida = f_salida

        def registrar_salida():
            # Recuperar fecha de salida guardada
            f_salida = getattr(btn_registrar, "fecha_salida", None)
            if f_salida is None:
                messagebox.showerror("Error", "Primero calcule el total.")
                return

            # Liberar habitación
            habitacion.disponible = True
            habitacion.nombre = ""
            habitacion.apellidos = ""
            habitacion.documento = ""
            habitacion.fecha_ingreso = None

            messagebox.showinfo(
                "Salida registrada",
                "La habitación ha sido liberada y queda disponible."
            )
            win.destroy()

        btn_calcular.config(command=calcular_total)
        btn_registrar.config(command=registrar_salida)


if __name__ == "__main__":
    app = HotelApp()
    app.mainloop()
 