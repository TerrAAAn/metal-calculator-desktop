import tkinter as tk
from tkinter import ttk, messagebox
from src.domain.element import Element
from src.domain.material import Material
from src.utils.data_loaders import DataLoader

class ElementEditor:
    def __init__(self, parent, weight_calculator, area_calculator, data_loader, existing_element=None):
        self.parent = parent
        self.weight_calc = weight_calculator
        self.area_calc = area_calculator
        self.data_loader = data_loader
        self.existing_element = existing_element
        self.result = None

        self.window = tk.Toplevel(parent)
        self.window.title("Редактор элемента")
        self.window.geometry("600x600")

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.window, text="Тип элемента:").pack(pady=5)
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(self.window, 
                textvariable=self.type_var, 
                values= ["лист", "круг", "труба", "труба профильная", "уголок", "отвод", "переход", "балка", "швеллер", "заглушка"]
            )
        self.type_combo.pack(pady=5)
        self.type_combo.bind("<<ComboboxSelected>>", self.on_type_change)

        ttk.Label(self.window, text="Количество:").pack(pady=5)
        self.quantity_var = tk.StringVar(value=1)
        tk.Entry(self.window, textvariable=self.quantity_var).pack(pady=5)

        ttk.Label(self.window, text="Материал:").pack(pady=5)
        self.material_var = tk.StringVar()
        self.material_combo = ttk.Combobox(
                self.window, 
                textvariable=self.material_var,
                values=[]
                )
        self.material_combo.pack(pady=5)

        self.params_frame = ttk.Frame(self.window)
        self.params_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        bottom_frame = ttk.Frame(self.window)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        self.btn_cancel = ttk.Button(bottom_frame, text="Отмена", command=self.cancel)
        self.btn_cancel.pack(side=tk.RIGHT, padx=5)

        self.btn_save = ttk.Button(bottom_frame, text="Сохранить", command=self.save)
        self.btn_save.pack(side=tk.RIGHT, padx=5)

        self.load_materials()
                
    def load_materials(self):
        steels = self.data_loader.get('steel_grades.json')
        self.material_combo['values'] = list(steels.keys())
        if self.material_combo['values']:
            self.material_combo.current(0)

    def save(self):
        element_type = self.type_var.get()
        quantity = self.to_float(self.quantity_var.get())

        if quantity is None or quantity <= 0:
            messagebox.showerror("Ошибка", "Некорректное количество")
            return None

        material_name = self.material_var.get()

        materials = self.data_loader.get('steel_grades.json')
        density = materials[material_name]
        material_obj = Material(material_name, density)

        params = {}

        match element_type:
            case 'лист':
                try:
                    params = {
                        'length' : self.to_float(self.length_var.get()),
                        'width' : self.to_float(self.width_var.get()),
                        'thickness' : self.to_float(self.thickness_var.get())
                    }
                except ValueError:
                    messagebox.showerror("Ошибка", "Введите корректные значения")
                    return None
            case 'круг':
                try:
                    params = {
                        'd' : self.to_float(self.d_var.get()),
                        'length' : self.to_float(self.length_var.get()) * 1000
                    }
                except ValueError:
                    messagebox.showerror("Ошибка", "Введите корректные значения")
                    return None
            case 'труба':
                try:
                    params = {
                        'd' : self.to_float(self.d_var.get()),
                        'thickness' : self.to_float(self.thickness_var.get()),
                        'length' : self.to_float(self.length_var.get()) * 1000
                    }
                except ValueError:
                    messagebox.showerror("Ошибка", "Введите корректные значения")
                    return None
            case 'труба профильная':
                try:
                    params = {
                        'width' : self.to_float(self.width_var.get()),
                        'height' : self.to_float(self.height_var.get()),
                        'thickness' : self.to_float(self.thickness_var.get()),
                        'length' : self.to_float(self.length_var.get()) * 1000
                    }
                except ValueError:
                    messagebox.showerror("Ошибка", "Введите корректные значения")
                    return None
            case 'уголок':
                try:
                    params = {
                        'width_a' : self.to_float(self.width_a_var.get()),
                        'width_b' : self.to_float(self.width_b_var.get()),
                        'thickness' : self.to_float(self.thickness_var.get()),
                        'length' : self.to_float(self.length_var.get()) * 1000
                    }
                except ValueError:
                    messagebox.showerror("Ошибка", "Введите корректные значения")
                    return None
            case 'заглушка':
                try:
                    params = {
                        'd' : self.to_float(self.d_var.get()),
                        'thickness' : self.to_float(self.thickness_var.get())
                    }
                except ValueError:
                    messagebox.showerror("Ошибка", "Введите корректные значения")
                    return None
            case 'отвод' | 'переход':
                params = {
                    'size' : self.size_var.get()
                }
            case 'балка' | 'швеллер':
                try:
                    params = {
                        'size' : self.size_var.get(),
                        'length' : self.to_float(self.length_var.get()) # Параметры за 1 м!!!
                    }
                except ValueError:
                    messagebox.showerror("Ошибка", "Введите корректные значения")
                    return None

        if not params:
            messagebox.showerror("Ошибка", "Введите корректные значения")
            return None
        if element_type in ("отвод", "переход", "балка", "швеллер"):
            if not params.get("size"):
                messagebox.showerror("Ошибка", "Выберите типоразмер")
                return None
            
        self.result = Element(
            element_type=element_type,
            quantity= quantity,
            material=material_obj,
            params=params
        )

        self.window.destroy()

    def cancel(self):
        self.result = None
        self.window.destroy()

    def on_type_change(self, event=None):
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        
        element_type = self.type_var.get()

        match element_type:
            case "лист":
                self.create_sheet_fields()
            case "круг":
                self.create_circle_fields()
            case "труба":
                self.create_tube_fields()
            case "труба профильная":
                self.create_prof_fields()
            case "уголок":
                self.create_angle_fields()
            case "заглушка":
                self.create_cap_fields()
            case "отвод":
                self.create_fittings_fields("elbows.json")
            case "переход":
                self.create_fittings_fields("reducers.json")
            case "швеллер":
                self.create_beams_channels_fields("channels.json")
            case "балка":
                self.create_beams_channels_fields('beams.json')
            case _:
                pass

    def create_sheet_fields(self):
        ttk.Label(self.params_frame, text="Длина (мм):").grid(row=0, column=0)
        self.length_var = tk.StringVar()
        tk.Entry(self.params_frame, textvariable=self.length_var).grid(row=0, column=1)

        ttk.Label(self.params_frame, text="Ширина (мм):").grid(row=1, column=0)
        self.width_var = tk.StringVar()
        tk.Entry(self.params_frame, textvariable=self.width_var).grid(row=1, column=1)

        ttk.Label(self.params_frame, text="Толщина (мм):").grid(row=2, column=0)
        self.thickness_var = tk.StringVar()
        tk.Entry(self.params_frame, textvariable=self.thickness_var).grid(row=2, column=1)

    def create_circle_fields(self):
        ttk.Label(self.params_frame, text="Диаметр (мм):").grid(row=0, column=0)
        self.d_var = tk.StringVar()
        tk.Entry(self.params_frame, textvariable=self.d_var).grid(row=0, column=1)

        ttk.Label(self.params_frame, text="Длина (м):").grid(row=1, column=0)
        self.length_var = tk.StringVar()
        tk.Entry(self.params_frame, textvariable=self.length_var).grid(row=1, column=1)

    def create_tube_fields(self):
        ttk.Label(self.params_frame, text="Диаметр (мм):").grid(row=0, column=0)
        self.d_var = tk.StringVar()
        tk.Entry(self.params_frame, textvariable=self.d_var).grid(row=0, column=1)

        ttk.Label(self.params_frame, text="Толщина (мм):").grid(row=1, column=0)
        self.thickness_var = tk.StringVar()
        tk.Entry(self.params_frame, textvariable=self.thickness_var).grid(row=1, column=1)

        ttk.Label(self.params_frame, text="Длина (м):").grid(row=2, column=0)
        self.length_var = tk.StringVar()
        tk.Entry(self.params_frame, textvariable=self.length_var).grid(row=2, column=1)
    
    def create_prof_fields(self):
        ttk.Label(self.params_frame, text="Ширина профиля (мм):").grid(row=0, column=0)
        self.width_var = tk.StringVar()
        tk.Entry(self.params_frame, textvariable=self.width_var).grid(row=0, column=1)

        ttk.Label(self.params_frame, text="Высота профиля (мм):").grid(row=1, column=0)
        self.height_var = tk.StringVar()
        tk.Entry(self.params_frame, textvariable=self.height_var).grid(row=1, column=1)

        ttk.Label(self.params_frame, text="Толщина (мм):").grid(row=2, column=0)
        self.thickness_var = tk.StringVar()
        tk.Entry(self.params_frame, textvariable=self.thickness_var).grid(row=2, column=1)

        ttk.Label(self.params_frame, text="Длина (м):").grid(row=3, column=0)
        self.length_var = tk.StringVar()
        tk.Entry(self.params_frame, textvariable=self.length_var).grid(row=3, column=1)

    def create_angle_fields(self):
        ttk.Label(self.params_frame, text="Ширина полки 1 (мм):").grid(row=0, column=0)
        self.width_a_var = tk.StringVar()
        tk.Entry(self.params_frame, textvariable=self.width_a_var).grid(row=0, column=1)

        ttk.Label(self.params_frame, text="Ширина полки 2 (мм):").grid(row=1, column=0)
        self.width_b_var = tk.StringVar()
        tk.Entry(self.params_frame, textvariable=self.width_b_var).grid(row=1, column=1)

        ttk.Label(self.params_frame, text="Толщина (мм):").grid(row=2, column=0)
        self.thickness_var = tk.StringVar()
        tk.Entry(self.params_frame, textvariable=self.thickness_var).grid(row=2, column=1)

        ttk.Label(self.params_frame, text="Длина (м):").grid(row=3, column=0)
        self.length_var = tk.StringVar()
        tk.Entry(self.params_frame, textvariable=self.length_var).grid(row=3, column=1)
    
    def create_cap_fields(self):
        ttk.Label(self.params_frame, text="Диаметр (мм):").grid(row=0, column=0)
        self.d_var = tk.StringVar()
        tk.Entry(self.params_frame, textvariable=self.d_var).grid(row=0, column=1)

        ttk.Label(self.params_frame, text="Толщина (мм):").grid(row=1, column=0)
        self.thickness_var = tk.StringVar()
        tk.Entry(self.params_frame, textvariable=self.thickness_var).grid(row=1, column=1)

    def create_fittings_fields(self, file_name):
        data = self.data_loader.get(file_name)
        sizes = list(data['weight'].keys())

        ttk.Label(self.params_frame, text="Типоразмер:").grid(row=0, column=0, sticky=tk.W, pady=5)

        self.size_var = tk.StringVar()
        self.size_combo = ttk.Combobox(self.params_frame, textvariable=self.size_var, values=sizes, width=20)
        self.size_combo.grid(row=0, column=1, padx=5, pady=5)

        if sizes:
            self.size_combo.current(0)

    def create_beams_channels_fields(self, file_name):
        data = self.data_loader.get(file_name)
        sizes = list(data['weight'].keys())

        ttk.Label(self.params_frame, text="Длина (м):").grid(row=0, column=0)
        self.length_var = tk.StringVar()
        tk.Entry(self.params_frame, textvariable=self.length_var).grid(row=0, column=1)

        ttk.Label(self.params_frame, text="Типоразмер:").grid(row=1, column=0, sticky=tk.W, pady=5)

        self.size_var = tk.StringVar()
        self.size_combo = ttk.Combobox(self.params_frame, textvariable=self.size_var, values=sizes, width=20)
        self.size_combo.grid(row=1, column=1, padx=5, pady=5)

        if sizes:
            self.size_combo.current(0)

    def to_float(self, value):
        if not value or not str(value).strip():
            return None
        normalized = str(value).strip().replace(',', '.')
        return float(normalized)