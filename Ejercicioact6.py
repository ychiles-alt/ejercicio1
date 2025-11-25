import os
import re
import tkinter as tk
from tkinter import messagebox

class Persona:
    def __init__(self, nombre: str, telefono: str, correo: str) -> None:
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo

class ContactBook:
    def __init__(self, filename: str = "archivo.txt") -> None:
        self.filename = filename
        if not os.path.exists(self.filename):
            open(self.filename, "w").close()

    def _load_contacts(self) -> list:
        contactos = []
        with open(self.filename, "r", encoding="utf-8") as file:
            for linea in file:
                linea = linea.strip()
                if not linea:
                    continue
                try:
                    nombre, telefono, correo = linea.split(",")
                    contactos.append(Persona(nombre, telefono, correo))
                except ValueError:
                    # si hay una línea mala la ignoramos
                    continue
        return contactos

    def _save_contacts(self, contactos: list) -> None:
        with open(self.filename, "w", encoding="utf-8") as file:
            for p in contactos:
                file.write(f"{p.nombre},{p.telefono},{p.correo}\n")

    def _validar_datos(self, nombre: str, telefono: str, correo: str, validar_duplicado=True) -> None:
        if telefono and not telefono.isdigit():
            raise ValueError("El teléfono debe contener solo números.")

        if correo and not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", correo):
            raise ValueError("Correo mal digitado.")

        if validar_duplicado and telefono:
            contactos = self._load_contacts()
            for p in contactos:
                if p.telefono == telefono:
                    raise ValueError("Ya existe un contacto con ese teléfono.")

    # --------- CRUD ---------

    def crear_contacto(self, nombre: str, telefono: str, correo: str) -> None:
        self._validar_datos(nombre, telefono, correo, validar_duplicado=True)
        contactos = self._load_contacts()
        contactos.append(Persona(nombre, telefono, correo))
        self._save_contacts(contactos)

    def listar_contactos(self) -> list:
        return self._load_contacts()

    def actualizar_contacto(self, telefono_original: str, nuevo_nombre: str, nuevo_telefono: str, nuevo_correo: str) -> None:
        contactos = self._load_contacts()
        encontrado = False

        # validar datos solo si se cambian
        tel_validar = nuevo_telefono or ""
        correo_validar = nuevo_correo or ""
        if tel_validar or correo_validar:
            # no queremos que dispare duplicado con el mismo teléfono original
            self._validar_datos(nuevo_nombre, tel_validar, correo_validar, validar_duplicado=False)

        for p in contactos:
            if p.telefono == telefono_original:
                encontrado = True
                if nuevo_nombre:
                    p.nombre = nuevo_nombre
                if nuevo_telefono:
                    # verificar duplicado solo si cambia de teléfono
                    if nuevo_telefono != telefono_original:
                        self._validar_datos("", nuevo_telefono, "", validar_duplicado=True)
                    p.telefono = nuevo_telefono
                if nuevo_correo:
                    self._validar_datos("", "", nuevo_correo, validar_duplicado=False)
                    p.correo = nuevo_correo
                break

        if not encontrado:
            raise ValueError("Contacto no encontrado.")

        self._save_contacts(contactos)

    def borrar_contacto(self, telefono: str) -> None:
        contactos = self._load_contacts()
        nuevos = [p for p in contactos if p.telefono != telefono]
        if len(nuevos) == len(contactos):
            raise ValueError("Contacto no encontrado.")
        self._save_contacts(nuevos)

class ContactApp:
    def __init__(self, root: tk.Tk, book: ContactBook) -> None:
        self.root = root
        self.book = book
        self.root.title("Agenda de contactos")
        self.root.geometry("500x500")

        self.pantalla = tk.Frame(self.root, bg="#A3A3A3")
        self.pantalla.place(x=0, y=28, width=500, height=470)

        # barra de botones CRUD
        tk.Button(self.root, text="Crear", command=self.crear_contacto_view, bg="#D6F7FF", width=10).place(x=0, y=0)
        tk.Button(self.root, text="Mostrar", command=self.mostrar_contactos_view, bg="#D6F7FF", width=10).place(x=80, y=0)
        tk.Button(self.root, text="Actualizar", command=self.actualizar_contacto_view, bg="#D6F7FF", width=10).place(x=160, y=0)
        tk.Button(self.root, text="Borrar", command=self.borrar_contacto_view, bg="#D6F7FF", width=10).place(x=240, y=0)

    def limpiar_pantalla(self) -> None:
        for widget in self.pantalla.winfo_children():
            widget.destroy()

    # --------- Vistas ---------

    def crear_contacto_view(self) -> None:
        self.limpiar_pantalla()

        nombre_entry = tk.Entry(self.pantalla, bg="#D6F7FF", width=40)
        nombre_entry.insert(0, "Nombre")
        nombre_entry.place(x=20, y=20)

        telefono_entry = tk.Entry(self.pantalla, bg="#D6F7FF", width=40)
        telefono_entry.insert(0, "Telefono")
        telefono_entry.place(x=20, y=50)

        correo_entry = tk.Entry(self.pantalla, bg="#D6F7FF", width=40)
        correo_entry.insert(0, "Correo")
        correo_entry.place(x=20, y=80)

        def on_enviar():
            try:
                self.book.crear_contacto(
                    nombre_entry.get().strip(),
                    telefono_entry.get().strip(),
                    correo_entry.get().strip()
                )
                messagebox.showinfo("Éxito", "Contacto creado")
                self.limpiar_pantalla()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.pantalla, text="Enviar", command=on_enviar, bg="#D6F7FF", width=10).place(x=20, y=110)
        tk.Button(self.pantalla, text="Cerrar", command=self.limpiar_pantalla, bg="#D6F7FF", width=10).place(x=110, y=110)

    def mostrar_contactos_view(self) -> None:
        self.limpiar_pantalla()
        contactos = self.book.listar_contactos()

        for p in contactos:
            bot = tk.Button(self.pantalla, text=f"{p.nombre}, {p.telefono}, {p.correo}",
                            state="disabled", relief="solid", bg="#D6F7FF", width=40, anchor="w")
            bot.pack(pady=2)

        tk.Button(self.pantalla, text="Cerrar", command=self.limpiar_pantalla,
                  bg="#D6F7FF", width=40, relief="solid").pack(pady=10)

    def actualizar_contacto_view(self) -> None:
        self.limpiar_pantalla()

        telefono_original_entry = tk.Entry(self.pantalla, bg="#D6F7FF", width=40)
        telefono_original_entry.insert(0, "Telefono del contacto")
        telefono_original_entry.place(x=20, y=20)

        nombre_entry = tk.Entry(self.pantalla, bg="#D6F7FF", width=40)
        nombre_entry.insert(0, "Nuevo nombre (opcional)")
        nombre_entry.place(x=20, y=50)

        telefono_entry = tk.Entry(self.pantalla, bg="#D6F7FF", width=40)
        telefono_entry.insert(0, "Nuevo telefono (opcional)")
        telefono_entry.place(x=20, y=80)

        correo_entry = tk.Entry(self.pantalla, bg="#D6F7FF", width=40)
        correo_entry.insert(0, "Nuevo correo (opcional)")
        correo_entry.place(x=20, y=110)

        def on_cambiar():
            try:
                self.book.actualizar_contacto(
                    telefono_original_entry.get().strip(),
                    nombre_entry.get().strip(),
                    telefono_entry.get().strip(),
                    correo_entry.get().strip()
                )
                messagebox.showinfo("Éxito", "Contacto actualizado")
                self.limpiar_pantalla()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.pantalla, text="Cambiar", command=on_cambiar, bg="#D6F7FF", width=10).place(x=20, y=140)
        tk.Button(self.pantalla, text="Cerrar", command=self.limpiar_pantalla, bg="#D6F7FF", width=10).place(x=110, y=140)

    def borrar_contacto_view(self) -> None:
        self.limpiar_pantalla()

        telefono_entry = tk.Entry(self.pantalla, bg="#D6F7FF", width=40)
        telefono_entry.insert(0, "Telefono del contacto")
        telefono_entry.place(x=20, y=20)

        def on_borrar():
            try:
                self.book.borrar_contacto(telefono_entry.get().strip())
                messagebox.showinfo("Éxito", "Contacto borrado")
                self.limpiar_pantalla()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.pantalla, text="Borrar", command=on_borrar, bg="#D6F7FF", width=10).place(x=20, y=50)
        tk.Button(self.pantalla, text="Cerrar", command=self.limpiar_pantalla, bg="#D6F7FF", width=10).place(x=110, y=50)

if __name__ == "__main__":
    root = tk.Tk()
    book = ContactBook("archivo.txt")
    app = ContactApp(root, book)
    root.mainloop()
