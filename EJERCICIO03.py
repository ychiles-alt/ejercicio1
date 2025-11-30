import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry  # pip install tkcalendar


class AgendaApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Agenda de contactos")
        self.geometry("500x500")

        # ---- CAMPOS SUPERIORES (FORMULARIO) ----
        frame = tk.Frame(self, padx=10, pady=10)
        frame.pack(fill="x")

        # Variables
        self.nombres_var = tk.StringVar()
        self.apellidos_var = tk.StringVar()
        self.direccion_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.correo_var = tk.StringVar()

        fila = 0

        # Nombres
        tk.Label(frame, text="Nombres:").grid(row=fila, column=0, sticky="e", pady=5)
        tk.Entry(frame, textvariable=self.nombres_var).grid(row=fila, column=1, sticky="we")
        fila += 1

        # Apellidos
        tk.Label(frame, text="Apellidos:").grid(row=fila, column=0, sticky="e", pady=5)
        tk.Entry(frame, textvariable=self.apellidos_var).grid(row=fila, column=1, sticky="we")
        fila += 1

        # Fecha de nacimiento (DatePicker)
        tk.Label(frame, text="Fecha de nacimiento:").grid(row=fila, column=0, sticky="e", pady=5)
        self.fecha_nacimiento = DateEntry(frame, date_pattern="dd/mm/yyyy")
        self.fecha_nacimiento.grid(row=fila, column=1, sticky="we")
        fila += 1

        # Dirección
        tk.Label(frame, text="Dirección:").grid(row=fila, column=0, sticky="e", pady=5)
        tk.Entry(frame, textvariable=self.direccion_var).grid(row=fila, column=1, sticky="we")
        fila += 1

        # Teléfono
        tk.Label(frame, text="Teléfono:").grid(row=fila, column=0, sticky="e", pady=5)
        tk.Entry(frame, textvariable=self.telefono_var).grid(row=fila, column=1, sticky="we")
        fila += 1

        # Correo
        tk.Label(frame, text="Correo electrónico:").grid(row=fila, column=0, sticky="e", pady=5)
        tk.Entry(frame, textvariable=self.correo_var).grid(row=fila, column=1, sticky="we")
        fila += 1

        frame.columnconfigure(1, weight=1)

        # Botón Agregar
        tk.Button(frame, text="Agregar", command=self.agregar_contacto)\
            .grid(row=fila, column=0, columnspan=2, pady=10)

        # ---- LISTA DE CONTACTOS (ListView → Listbox) ----
        tk.Label(self, text="Contactos agregados:", font=("Arial", 12))\
            .pack(anchor="w", padx=10)

        self.lista = tk.Listbox(self, height=12)
        self.lista.pack(fill="both", expand=True, padx=10, pady=10)

    def agregar_contacto(self):
        nombres = self.nombres_var.get().strip()
        apellidos = self.apellidos_var.get().strip()
        fecha = self.fecha_nacimiento.get()
        direccion = self.direccion_var.get().strip()
        telefono = self.telefono_var.get().strip()
        correo = self.correo_var.get().strip()

        # Validación: todos obligatorios
        if not (nombres and apellidos and fecha and direccion and telefono and correo):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Texto que se muestra en la lista
        contacto = f"{nombres} {apellidos} | {fecha} | {telefono} | {correo}"

        # Insertar en Listbox
        self.lista.insert(tk.END, contacto)

        # Limpiar campos (dejo la fecha igual, puedes cambiarlo si quieres)
        self.nombres_var.set("")
        self.apellidos_var.set("")
        self.direccion_var.set("")
        self.telefono_var.set("")
        self.correo_var.set("")
        # Si quisieras reiniciar la fecha a hoy:
        # from datetime import date
        # self.fecha_nacimiento.set_date(date.today())


if __name__ == "__main__":
    app = AgendaApp()
    app.mainloop()
