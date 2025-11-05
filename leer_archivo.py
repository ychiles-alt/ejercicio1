# leer_archivo_gui.py
# GUI con Tkinter para leer archivos de texto (versión OOP y equivalente al ejemplo de Java).

import io
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path


DEFAULT_TEXT = "\n".join(f"Línea {i}" for i in range(1, 11)) + "\n"


def asegurar_archivo(ruta: Path, encoding: str = "utf-8") -> None:
    """Crea un archivo de ejemplo si no existe."""
    if not ruta.exists():
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(DEFAULT_TEXT, encoding=encoding)


class LeerArchivo:
    """
    Clase análoga al ejemplo Java:
    - FileInputStream  -> apertura binaria ('rb')
    - BufferedReader   -> io.BufferedReader sobre el binario
    - InputStreamReader-> io.TextIOWrapper para decodificar a texto
    """
    def __init__(self, ruta: Path, encoding: str = "utf-8"):
        self.ruta = Path(ruta)
        self.encoding = encoding

    def leer_todo(self) -> str:
        with self.ruta.open("rb") as raw:               # FileInputStream
            buffered = io.BufferedReader(raw)           # BufferedReader
            text = io.TextIOWrapper(                    # InputStreamReader
                buffered, encoding=self.encoding, errors="replace", newline=None
            )
            try:
                return text.read()
            finally:
                # Evita cierre doble de 'raw' en algunos entornos
                text.detach()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lectura de archivos - Ejercicio 6.8 (GUI)")
        self.geometry("720x520")
        self.minsize(560, 400)

        # Ruta por defecto (junto al script)
        self.default_path = Path("prueba.txt")
        asegurar_archivo(self.default_path)

        self._build_ui()

    def _build_ui(self):
        # Frame superior (botones)
        top = ttk.Frame(self, padding=10)
        top.pack(side=tk.TOP, fill=tk.X)

        self.encoding_var = tk.StringVar(value="utf-8")

        ttk.Button(top, text="Leer archivo por defecto",
                   command=self.leer_por_defecto).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(top, text="Abrir archivo…",
                   command=self.abrir_archivo).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(top, text="Limpiar",
                   command=self.limpiar).pack(side=tk.LEFT, padx=(0, 8))

        ttk.Label(top, text="Encoding:").pack(side=tk.LEFT, padx=(16, 4))
        ttk.Entry(top, textvariable=self.encoding_var, width=12).pack(side=tk.LEFT)

        # Área de texto con scroll
        mid = ttk.Frame(self, padding=(10, 0, 10, 10))
        mid.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.text = tk.Text(mid, wrap="none", undo=True)
        self.text.configure(font=("Consolas", 11))

        yscroll = ttk.Scrollbar(mid, orient="vertical", command=self.text.yview)
        xscroll = ttk.Scrollbar(mid, orient="horizontal", command=self.text.xview)
        self.text.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

        self.text.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")

        mid.columnconfigure(0, weight=1)
        mid.rowconfigure(0, weight=1)

        # Barra de estado
        self.status = tk.StringVar(value=f"Listo. Archivo por defecto: {self.default_path.resolve()}")
        statusbar = ttk.Label(self, textvariable=self.status, anchor="w", padding=(10, 4))
        statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def leer_por_defecto(self):
        self._leer_y_mostrar(self.default_path)

    def abrir_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Selecciona un archivo de texto",
            filetypes=[("Archivos de texto", "*.txt;*.log;*.md;*.csv;*.json;*.py;*.java;*.*")],
            initialdir=str(Path.cwd())
        )
        if not ruta:
            return
        self._leer_y_mostrar(Path(ruta))

    def limpiar(self):
        self.text.delete("1.0", tk.END)
        self.status.set("Limpio.")

    def _leer_y_mostrar(self, ruta: Path):
        try:
            lector = LeerArchivo(ruta, encoding=self.encoding_var.get().strip() or "utf-8")
            contenido = lector.leer_todo()
            # Normalizamos fin de línea para evitar sobrescritura visual por '\r'
            contenido = contenido.replace("\r\n", "\n").replace("\r", "\n")
            self.text.delete("1.0", tk.END)
            self.text.insert("1.0", contenido)
            self.status.set(f"Leído: {ruta.resolve()}")
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo:\n{ruta}")
            self.status.set("Error: archivo no encontrado.")
        except PermissionError:
            messagebox.showerror("Error", f"Permiso denegado al leer:\n{ruta}")
            self.status.set("Error: permiso denegado.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{e}")
            self.status.set("Error inesperado.")

if __name__ == "__main__":
    App().mainloop()



if __name__ == "__main__":
    LeerArchivo.main()

