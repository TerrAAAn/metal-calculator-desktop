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

        ttk.Label(self.window, text="Количество:").pack(pady=5)
        self.quantity_var = tk.IntVar(value=1)
        tk.Entry(self.window, textvariable=self.quantity_var).pack(pady=5)

        ttk.Label(self.window, text="Материал:").pack(pady=5)
        self.material_var = tk.StringVar()
        self.material_combo = ttk.Combobox(
                self.window, 
                textvariable=self.material_var,
                values=[]
                )
        self.material_combo.pack(pady=5)

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
        quantity = self.quantity_var.get()
        material_name = self.material_var.get()
        materials = self.data_loader.get('steel_grades.json')
        density = materials[material_name]
        material_obj = Material(material_name, density)
        self.result = Element(
            element_type=element_type,
            quantity= quantity,
            material=material_obj,
            params={}
        )
        self.window.destroy()

    def cancel(self):
        self.result = None
        self.window.destroy()