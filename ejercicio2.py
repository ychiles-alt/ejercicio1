import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
from math import pi

# ================== MODELO (POO) ==================

class FiguraGeometrica(ABC):
    @abstractmethod
    def volumen(self) -> float: ...
    @abstractmethod
    def superficie(self) -> float: ...

class Cilindro(FiguraGeometrica):
    def __init__(self, radio: float, altura: float):
        self.radio = radio
        self.altura = altura
    def volumen(self) -> float:
        return pi * (self.radio ** 2) * self.altura
    def superficie(self) -> float:
        return 2 * pi * self.radio * (self.radio + self.altura)

class Esfera(FiguraGeometrica):
    def __init__(self, radio: float):
        self.radio = radio
    def volumen(self) -> float:
        return (4.0 / 3.0) * pi * (self.radio ** 3)
    def superficie(self) -> float:
        return 4 * pi * (self.radio ** 2)

class Piramide(FiguraGeometrica):
    """Pirámide de base cuadrada (base = lado, apotema = slant height)."""
    def __init__(self, base: float, altura: float, apotema: float):
        self.base = base
        self.altura = altura
        self.apotema = apotema
    def volumen(self) -> float:
        return (1.0 / 3.0) * (self.base ** 2) * self.altura
    def superficie(self) -> float:
        area_base = self.base ** 2
        perimetro = 4 * self.base
        area_lateral = 0.5 * perimetro * self.apotema
        return area_base + area_lateral

# ================== VISTA / CONTROL (Tkinter) ==================

class AppFiguras:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Volumen y Superficie de Figuras")
        self.root.resizable(False, False)

        cont = ttk.Frame(root, padding=10)
        cont.grid(row=0, column=0, sticky="nsew")

        self.notebook = ttk.Notebook(cont)
        self.notebook.grid(row=0, column=0)

        self._init_tab_cilindro()
        self._init_tab_esfera()
        self._init_tab_piramide()

    # ---------- Helpers ----------
    def _leer_float(self, entry: ttk.Entry, nombre: str) -> float:
        txt = entry.get().strip().replace(",", ".")
        if not txt:
            raise ValueError(f"Ingrese {nombre}.")
        try:
            val = float(txt)
        except ValueError:
            raise ValueError(f"{nombre} debe ser numérico.")
        if val <= 0:
            raise ValueError(f"{nombre} debe ser mayor que 0.")
        return val

    def _f(self, x: float) -> str:
        return f"{x:.2f}".replace(".", ",")

    # ---------- Tab: Cilindro ----------
    def _init_tab_cilindro(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="Cilindro")

        ttk.Label(tab, text="Radio (cm):").grid(row=0, column=0, sticky="e", padx=(0,8), pady=3)
        ttk.Label(tab, text="Altura (cm):").grid(row=1, column=0, sticky="e", padx=(0,8), pady=3)

        self.c_r = ttk.Entry(tab, width=12)
        self.c_h = ttk.Entry(tab, width=12)
        self.c_r.grid(row=0, column=1, pady=3)
        self.c_h.grid(row=1, column=1, pady=3)

        btns = ttk.Frame(tab); btns.grid(row=2, column=0, columnspan=2, pady=6)
        ttk.Button(btns, text="Calcular", command=self._calc_cilindro).grid(row=0, column=0, padx=(0,6))
        ttk.Button(btns, text="Limpiar", command=self._clear_cilindro).grid(row=0, column=1)

        self.c_res_v = ttk.Label(tab, text="Volumen (cm³) = ")
        self.c_res_s = ttk.Label(tab, text="Superficie (cm²) = ")
        self.c_res_v.grid(row=3, column=0, columnspan=2, sticky="w", pady=(6,0))
        self.c_res_s.grid(row=4, column=0, columnspan=2, sticky="w")

    def _calc_cilindro(self):
        try:
            r = self._leer_float(self.c_r, "el radio (cm)")
            h = self._leer_float(self.c_h, "la altura (cm)")
            fig = Cilindro(r, h)
            self.c_res_v.config(text=f"Volumen (cm³) = {self._f(fig.volumen())} cm³")
            self.c_res_s.config(text=f"Superficie (cm²) = {self._f(fig.superficie())} cm²")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _clear_cilindro(self):
        self.c_r.delete(0, tk.END); self.c_h.delete(0, tk.END)
        self.c_res_v.config(text="Volumen (cm³) = "); self.c_res_s.config(text="Superficie (cm²) = ")

    # ---------- Tab: Esfera ----------
    def _init_tab_esfera(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="Esfera")

        ttk.Label(tab, text="Radio (cm):").grid(row=0, column=0, sticky="e", padx=(0,8), pady=3)
        self.e_r = ttk.Entry(tab, width=12); self.e_r.grid(row=0, column=1, pady=3)

        btns = ttk.Frame(tab); btns.grid(row=1, column=0, columnspan=2, pady=6)
        ttk.Button(btns, text="Calcular", command=self._calc_esfera).grid(row=0, column=0, padx=(0,6))
        ttk.Button(btns, text="Limpiar", command=self._clear_esfera).grid(row=0, column=1)

        self.e_res_v = ttk.Label(tab, text="Volumen (cm³) = ")
        self.e_res_s = ttk.Label(tab, text="Superficie (cm²) = ")
        self.e_res_v.grid(row=2, column=0, columnspan=2, sticky="w", pady=(6,0))
        self.e_res_s.grid(row=3, column=0, columnspan=2, sticky="w")

    def _calc_esfera(self):
        try:
            r = self._leer_float(self.e_r, "el radio (cm)")
            fig = Esfera(r)
            self.e_res_v.config(text=f"Volumen (cm³) = {self._f(fig.volumen())} cm³")
            self.e_res_s.config(text=f"Superficie (cm²) = {self._f(fig.superficie())} cm²")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _clear_esfera(self):
        self.e_r.delete(0, tk.END)
        self.e_res_v.config(text="Volumen (cm³) = "); self.e_res_s.config(text="Superficie (cm²) = ")

    # ---------- Tab: Pirámide ----------
    def _init_tab_piramide(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="Pirámide (base cuadrada)")

        ttk.Label(tab, text="Base (cm):").grid(row=0, column=0, sticky="e", padx=(0,8), pady=3)
        ttk.Label(tab, text="Altura (cm):").grid(row=1, column=0, sticky="e", padx=(0,8), pady=3)
        ttk.Label(tab, text="Apotema (cm):").grid(row=2, column=0, sticky="e", padx=(0,8), pady=3)

        self.p_b = ttk.Entry(tab, width=12)
        self.p_h = ttk.Entry(tab, width=12)
        self.p_a = ttk.Entry(tab, width=12)
        self.p_b.grid(row=0, column=1, pady=3)
        self.p_h.grid(row=1, column=1, pady=3)
        self.p_a.grid(row=2, column=1, pady=3)

        btns = ttk.Frame(tab); btns.grid(row=3, column=0, columnspan=2, pady=6)
        ttk.Button(btns, text="Calcular", command=self._calc_piramide).grid(row=0, column=0, padx=(0,6))
        ttk.Button(btns, text="Limpiar", command=self._clear_piramide).grid(row=0, column=1)

        self.p_res_v = ttk.Label(tab, text="Volumen (cm³) = ")
        self.p_res_s = ttk.Label(tab, text="Superficie (cm²) = ")
        self.p_res_v.grid(row=4, column=0, columnspan=2, sticky="w", pady=(6,0))
        self.p_res_s.grid(row=5, column=0, columnspan=2, sticky="w")

    def _calc_piramide(self):
        try:
            b = self._leer_float(self.p_b, "la base (cm)")
            h = self._leer_float(self.p_h, "la altura (cm)")
            a = self._leer_float(self.p_a, "la apotema (cm)")
            fig = Piramide(b, h, a)
            self.p_res_v.config(text=f"Volumen (cm³) = {self._f(fig.volumen())} cm³")
            self.p_res_s.config(text=f"Superficie (cm²) = {self._f(fig.superficie())} cm²")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _clear_piramide(self):
        self.p_b.delete(0, tk.END); self.p_h.delete(0, tk.END); self.p_a.delete(0, tk.END)
        self.p_res_v.config(text="Volumen (cm³) = "); self.p_res_s.config(text="Superficie (cm²) = ")

# ================== MAIN ==================
if __name__ == "__main__":
    root = tk.Tk()
    AppFiguras(root)
    root.mainloop()
