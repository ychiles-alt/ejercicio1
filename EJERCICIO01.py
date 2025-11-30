import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from dataclasses import dataclass
from typing import List
import os


@dataclass
class Empleado:
    nombre: str
    apellidos: str
    cargo: str
    genero: str
    salario_dia: float
    dias_trabajados: int
    otros_ingresos: float
    pagos_salud: float
    aporte_pension: float

    def salario_mensual(self) -> float:
        """
        Salario mensual = (días trabajados * sueldo por día)
                          + otros ingresos
                          - pagos por salud
                          - aporte pensiones
        """
        return (self.dias_trabajados * self.salario_dia) + \
               self.otros_ingresos - self.pagos_salud - self.aporte_pension


class NominaApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Nómina de Empleados")
        self.geometry("600x400")

        self.empleados: List[Empleado] = []

        # Barra de menús
        barra_menu = tk.Menu(self)
        menu_opciones = tk.Menu(barra_menu, tearoff=0)
        menu_opciones.add_command(label="Agregar empleado",
                                  command=self.ventana_agregar_empleado)
        menu_opciones.add_command(label="Calcular nómina",
                                  command=self.ventana_calcular_nomina)
        menu_opciones.add_command(label="Guardar archivo",
                                  command=self.guardar_archivo_nomina)
        barra_menu.add_cascade(label="Opciones", menu=menu_opciones)
        self.config(menu=barra_menu)

        # Mensaje principal
        label = tk.Label(self, text="Use el menú para gestionar la nómina.",
                         font=("Arial", 12))
        label.pack(expand=True)

    # ----------------- VENTANA: AGREGAR EMPLEADO -----------------
    def ventana_agregar_empleado(self):
        win = tk.Toplevel(self)
        win.title("Agregar empleado")
        win.geometry("500x420")
        win.grab_set()  # Bloquea la ventana principal mientras se usa esta

        frame = tk.Frame(win, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        # Variables
        nombre_var = tk.StringVar()
        apellidos_var = tk.StringVar()
        genero_var = tk.StringVar()  # para Radiobuttons

        salario_dia_var = tk.StringVar()
        dias_trabajados_var = tk.IntVar(value=1)
        otros_ingresos_var = tk.StringVar(value="0")
        salud_var = tk.StringVar(value="0")
        pension_var = tk.StringVar(value="0")

        # Nombre
        tk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky="e", pady=3)
        tk.Entry(frame, textvariable=nombre_var).grid(row=0, column=1, sticky="we", pady=3)

        # Apellidos
        tk.Label(frame, text="Apellidos:").grid(row=1, column=0, sticky="e", pady=3)
        tk.Entry(frame, textvariable=apellidos_var).grid(row=1, column=1, sticky="we", pady=3)

        # Cargo (Listbox)
        tk.Label(frame, text="Cargo:").grid(row=2, column=0, sticky="ne", pady=3)
        cargos = ["Directivo", "Estratégico", "Operativo"]
        lista_cargo = tk.Listbox(frame, height=3, exportselection=False)
        for c in cargos:
            lista_cargo.insert(tk.END, c)
        lista_cargo.selection_set(0)  # seleccionar el primero por defecto
        lista_cargo.grid(row=2, column=1, sticky="we", pady=3)

        # Género (Radiobuttons)
        tk.Label(frame, text="Género:").grid(row=3, column=0, sticky="e", pady=3)
        frame_genero = tk.Frame(frame)
        frame_genero.grid(row=3, column=1, sticky="w", pady=3)
        tk.Radiobutton(frame_genero, text="Masculino",
                       variable=genero_var, value="Masculino").pack(side="left")
        tk.Radiobutton(frame_genero, text="Femenino",
                       variable=genero_var, value="Femenino").pack(side="left")

        # Salario por día
        tk.Label(frame, text="Salario por día:").grid(row=4, column=0, sticky="e", pady=3)
        tk.Entry(frame, textvariable=salario_dia_var).grid(row=4, column=1, sticky="we", pady=3)

        # Días trabajados (Spinbox)
        tk.Label(frame, text="Días trabajados al mes:").grid(row=5, column=0, sticky="e", pady=3)
        spin_dias = tk.Spinbox(frame, from_=1, to=31, textvariable=dias_trabajados_var)
        spin_dias.grid(row=5, column=1, sticky="we", pady=3)

        # Otros ingresos
        tk.Label(frame, text="Otros ingresos:").grid(row=6, column=0, sticky="e", pady=3)
        tk.Entry(frame, textvariable=otros_ingresos_var).grid(row=6, column=1, sticky="we", pady=3)

        # Pagos por salud
        tk.Label(frame, text="Pagos por salud:").grid(row=7, column=0, sticky="e", pady=3)
        tk.Entry(frame, textvariable=salud_var).grid(row=7, column=1, sticky="we", pady=3)

        # Aporte pensiones
        tk.Label(frame, text="Aporte pensiones:").grid(row=8, column=0, sticky="e", pady=3)
        tk.Entry(frame, textvariable=pension_var).grid(row=8, column=1, sticky="we", pady=3)

        frame.columnconfigure(1, weight=1)

        # Botones
        frame_botones = tk.Frame(win, pady=10)
        frame_botones.pack()

        def guardar_empleado():
            nombre = nombre_var.get().strip()
            apellidos = apellidos_var.get().strip()
            if not nombre or not apellidos:
                messagebox.showerror("Error", "Nombre y apellidos son obligatorios.")
                return

            try:
                seleccion = lista_cargo.curselection()
                if not seleccion:
                    messagebox.showerror("Error", "Debe seleccionar un cargo.")
                    return
                cargo = lista_cargo.get(seleccion[0])

                genero = genero_var.get()
                if not genero:
                    messagebox.showerror("Error", "Debe seleccionar un género.")
                    return

                salario_dia = float(salario_dia_var.get().strip())
                dias_trabajados = int(dias_trabajados_var.get())
                otros_ingresos = float(otros_ingresos_var.get().strip())
                salud = float(salud_var.get().strip())
                pension = float(pension_var.get().strip())

            except ValueError:
                messagebox.showerror(
                    "Error de formato",
                    "Verifique que los campos numéricos tengan valores válidos."
                )
                return

            emp = Empleado(
                nombre=nombre,
                apellidos=apellidos,
                cargo=cargo,
                genero=genero,
                salario_dia=salario_dia,
                dias_trabajados=dias_trajados,
                otros_ingresos=otros_ingresos,
                pagos_salud=salud,
                aporte_pension=pension
            )
            self.empleados.append(emp)
            messagebox.showinfo("Éxito", "Empleado agregado correctamente.")
            win.destroy()

        def cancelar():
            win.destroy()

        tk.Button(frame_botones, text="Guardar", command=guardar_empleado).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Cancelar", command=cancelar).pack(side="left", padx=5)

    # ----------------- VENTANA: CALCULAR NÓMINA -----------------
    def ventana_calcular_nomina(self):
        if not self.empleados:
            messagebox.showinfo("Información", "No hay empleados registrados.")
            return

        win = tk.Toplevel(self)
        win.title("Nómina de empleados")
        win.geometry("700x400")
        win.grab_set()

        columns = ("nombre", "apellidos", "cargo", "genero", "salario_mensual")
        tree = ttk.Treeview(win, columns=columns, show="headings")
        tree.heading("nombre", text="Nombre")
        tree.heading("apellidos", text="Apellidos")
        tree.heading("cargo", text="Cargo")
        tree.heading("genero", text="Género")
        tree.heading("salario_mensual", text="Salario mensual")

        tree.column("nombre", width=120)
        tree.column("apellidos", width=150)
        tree.column("cargo", width=100)
        tree.column("genero", width=80)
        tree.column("salario_mensual", width=120, anchor="e")

        scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        total_nomina = 0.0
        for emp in self.empleados:
            salario = emp.salario_mensual()
            total_nomina += salario
            tree.insert("", tk.END, values=(
                emp.nombre,
                emp.apellidos,
                emp.cargo,
                emp.genero,
                f"{salario:.2f}"
            ))

        lbl_total = tk.Label(win, text=f"Total de la nómina: {total_nomina:.2f}",
                             font=("Arial", 12), pady=10)
        lbl_total.pack(side="bottom", fill="x")

    # ----------------- GUARDAR ARCHIVO NÓMINA.TXT -----------------
    def guardar_archivo_nomina(self):
        if not self.empleados:
            messagebox.showinfo("Información", "No hay empleados para guardar.")
            return

        carpeta = filedialog.askdirectory(
            title="Seleccione la carpeta donde guardar Nómina.txt"
        )
        if not carpeta:
            return  # canceló

        ruta_archivo = os.path.join(carpeta, "Nomina.txt")

        try:
            total_nomina = 0.0
            with open(ruta_archivo, "w", encoding="utf-8") as f:
                f.write("NÓMINA DE EMPLEADOS\n")
                f.write("===================\n\n")

                for i, emp in enumerate(self.empleados, start=1):
                    salario = emp.salario_mensual()
                    total_nomina += salario
                    f.write(f"Empleado {i}:\n")
                    f.write(f"  Nombre: {emp.nombre}\n")
                    f.write(f"  Apellidos: {emp.apellidos}\n")
                    f.write(f"  Cargo: {emp.cargo}\n")
                    f.write(f"  Género: {emp.genero}\n")
                    f.write(f"  Salario por día: {emp.salario_dia:.2f}\n")
                    f.write(f"  Días trabajados: {emp.dias_trabajados}\n")
                    f.write(f"  Otros ingresos: {emp.otros_ingresos:.2f}\n")
                    f.write(f"  Pagos por salud: {emp.pagos_salud:.2f}\n")
                    f.write(f"  Aporte pensiones: {emp.aporte_pension:.2f}\n")
                    f.write(f"  Salario mensual: {salario:.2f}\n")
                    f.write("\n")

                f.write("===================\n")
                f.write(f"TOTAL NÓMINA: {total_nomina:.2f}\n")

            messagebox.showinfo("Éxito", f"Nómina guardada en:\n{ruta_archivo}")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar el archivo:\n{e}")


if __name__ == "__main__":
    app = NominaApp()
    app.mainloop()
