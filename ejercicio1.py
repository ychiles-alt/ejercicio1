import tkinter as tk
from tkinter import ttk, messagebox
import statistics

class VentanaNotas:
    def __init__(self, root):
        self.root = root
        self.root.title("Notas")
        self.root.resizable(False, False)

        # ====== CONFIG ======
        self.USE_SAMPLE_STD = True   # True -> stdev (muestral), False -> pstdev (poblacional)

        # ====== CONTENEDOR ======
        cont = ttk.Frame(self.root, padding=10)
        cont.grid(row=0, column=0, sticky="nsew")

        ttk.Style().configure("TLabel", font=("Segoe UI", 9))
        ttk.Style().configure("TButton", padding=3)

        # ====== ENTRADAS ======
        self.entradas = []
        for i in range(5):
            ttk.Label(cont, text=f"Nota {i+1}:").grid(row=i, column=0, padx=(0,10), pady=3, sticky="e")
            e = ttk.Entry(cont, width=12, justify="left")
            e.grid(row=i, column=1, pady=3, sticky="we")
            self.entradas.append(e)

        # ====== BOTONES ======
        btn_frame = ttk.Frame(cont)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=(8,8))
        ttk.Button(btn_frame, text="Calcular", command=self.calcular).grid(row=0, column=0, padx=(0,6))
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar).grid(row=0, column=1)

        # ====== RESULTADOS ======
        self.lbl_prom = ttk.Label(cont, text="Promedio = ")
        self.lbl_std  = ttk.Label(cont, text="Desviación estándar = ")
        self.lbl_max  = ttk.Label(cont, text="Valor mayor = ")
        self.lbl_min  = ttk.Label(cont, text="Valor menor = ")

        self.lbl_prom.grid(row=6, column=0, columnspan=2, sticky="w", pady=(4,0))
        self.lbl_std.grid (row=7, column=0, columnspan=2, sticky="w")
        self.lbl_max.grid (row=8, column=0, columnspan=2, sticky="w")
        self.lbl_min.grid (row=9, column=0, columnspan=2, sticky="w")

        cont.columnconfigure(1, weight=1)

    # ---- helpers ----
    def _fmt(self, x):
        """Formatea a 2 decimales con coma."""
        if isinstance(x, float):
            return f"{x:.2f}".replace(".", ",")
        return str(x).replace(".", ",")

    def _leer_notas(self):
        """Leer y validar que las 5 notas (entre 0.0 y 5.0)."""
        notas = []
        for e in self.entradas:
            txt = e.get().strip().replace(",", ".")
            if txt == "":
                raise ValueError("Debe ingresar las 5 notas.")
            try:
                val = float(txt)
            except ValueError:
                raise ValueError("Todas las notas deben ser números.")
            if not (0.0 <= val <= 5.0):
                raise ValueError("Las notas deben estar entre 0.0 y 5.0.")
            notas.append(val)
        return notas

    # ---- acciones ----
    def calcular(self):
        try:
            notas = self._leer_notas()

            prom = sum(notas) / len(notas)
            if self.USE_SAMPLE_STD and len(notas) > 1:
                desv = statistics.stdev(notas)
            else:
                desv = statistics.pstdev(notas)

            mayor = max(notas)
            menor = min(notas)

            self.lbl_prom.config(text=f"Promedio = {self._fmt(prom)}")
            self.lbl_std.config (text=f"Desviación estándar = {self._fmt(desv)}")
            self.lbl_max.config (text=f"Valor mayor = {self._fmt(mayor)}")
            self.lbl_min.config (text=f"Valor menor = {self._fmt(menor)}")

        except ValueError as ex:
            messagebox.showerror("Error", str(ex))
        except Exception:
            messagebox.showerror("Error", "Verifique que todas las notas sean validas.")

    def limpiar(self):
        for e in self.entradas:
            e.delete(0, tk.END)
        self.lbl_prom.config(text="Promedio = ")
        self.lbl_std.config (text="Desviación estándar = ")
        self.lbl_max.config (text="Valor mayor = ")
        self.lbl_min.config (text="Valor menor = ")

# ====== main ======
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaNotas(root)
    root.mainloop()

