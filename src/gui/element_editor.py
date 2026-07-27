import tkinter as tk
from tkinter import ttk, messagebox
from src.domain.factory import create_element, restore_element, get_element_class
from src.utils.data_loaders import DataLoader

class Element_editor:
    def __init__(self, root, main_window, construction, edit_index=None):
        self.root = root
        self.main_window = main_window
        self.construction = construction
        self.edit_index = edit_index

        self.entries = {}
        self.param_frame = None

        self.window = tk.Toplevel(main_window)
        self.window.title("Создание / редактирование элемента")
        self.window.geometry("600x500")
        self.window.resizable(False, False)

        self.loader = DataLoader()

        self.REFERENCE_MAP = {
            "Балка": "beams.json",
            "Швеллер": "channels.json",
            "Отвод": "elbows.json",
            "Переход": "reducers.json",
        }

        self.create_widgets()

        if self.edit_index is not None:
            existing = self.construction.get_elements_list()[self.edit_index]
            self.type_var.set(existing.__class__.__name__)  # установить тип
            self.quantity_var.set(str(existing.quantity))
            self.type_combo.config(state="disabled")
            # Заполнить материал (если есть)
            if hasattr(existing, 'density'):
                # Найти материал по плотности
                materials = self.loader.get('steel_grades.json')
                for name, dens in materials.items():
                    if dens == existing.density:
                        self.material_var.set(name)
                        break

            self.on_type_change(None)  # создаём поля параметров

            for key, value in existing.params.items():
                if key in self.entries:
                    self.entries[key].set(str(value))

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="#1e3a8a")
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), foreground="#ffffff", background="#2563eb")
        style.map("Accent.TButton", background=[("active", "#1d4ed8")])
        style.configure("Del.TButton", font=("Segoe UI", 10, "bold"), foreground="#ffffff", background="#be2828")
        style.map("Del.TButton", background=[("active", "#9e2b2b")])
        style.configure("Redo.TButton", font=("Segoe UI", 10, "bold"), foreground="#ffffff", background="#acbe28")
        style.map("Redo.TButton", background=[("active", "#808b2e")])

        # Тулбар
        toolbar_frame = ttk.Frame(self.window)
        toolbar_frame.pack(fill=tk.X, padx=15, pady=10)

        self.btn_save = ttk.Button(toolbar_frame, text="Сохранить", command=self.on_save, style="Accent.TButton")
        self.btn_save.pack(side=tk.LEFT, padx=5)

        self.btn_cancel = ttk.Button(toolbar_frame, text="Отмена", command=self.on_cancel, style="Del.TButton")
        self.btn_cancel.pack(side=tk.LEFT, padx=5)

        ttk.Separator(self.window, orient='horizontal').pack(fill=tk.X, padx=15, pady=5)

        # Фрейм для статических полей (тип, количество, материал)
        top_frame = ttk.Frame(self.window)
        top_frame.pack(fill=tk.X, padx=15, pady=10)

        # Тип
        ttk.Label(top_frame, text="Тип элемента:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(
            top_frame,
            textvariable=self.type_var,
            values=["Труба", "Лист", "Балка", "Швеллер", "Уголок", "Круг", "Полоса", "Профильная труба", "Заглушка", "Отвод", "Переход"],
            width=20
        )
        self.type_combo.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        self.type_combo.bind("<<ComboboxSelected>>", self.on_type_change)

        # Количество
        ttk.Label(top_frame, text="Количество:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.quantity_var = tk.StringVar(value="1")
        tk.Entry(top_frame, textvariable=self.quantity_var, width=20).grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)

        # Материал
        ttk.Label(top_frame, text="Материал:").grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.material_var = tk.StringVar()
        self.material_combo = ttk.Combobox(top_frame, textvariable=self.material_var, width=20)
        self.material_combo.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        self.load_materials()

        ttk.Separator(self.window, orient='horizontal').pack(fill=tk.X, padx=15, pady=5)

        # Фрейм для динамических параметров
        self.param_frame = ttk.Frame(self.window)
        self.param_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    def on_save(self):
        element_type = self.type_var.get()

        if not element_type:
            messagebox.showerror("Ошибка", "Выберите тип элемента")
            return

        try:
            quantity = self.to_float(self.quantity_var.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Количество должно быть числом")
            return

        if quantity <= 0:
            messagebox.showerror("Ошибка", "Количество должно быть больше 0")
            return

        params = {}
        for key, var in self.entries.items():
            raw = var.get().strip()
            try:
                params[key] = self.to_float(raw)
            except ValueError:
                params[key] = raw

        

        material_name = self.material_var.get()
        materials = self.loader.get('steel_grades.json')
        density = materials.get(material_name)

        if density is None:
            messagebox.showerror("Ошибка", "Выберите материал")
            return  # если материал "Ст3 7850" -> берём число

        # Создаём элемент
        if self.validate_ref_elements(element_type, params):
            element = create_element(element_type, params, density, quantity)

            if self.edit_index is None:
                self.construction.add_element(element)
            else:
                self.construction.replace_element(self.edit_index, element)

            self.window.destroy()
            self.root.refresh_elements_listbox()

    def on_cancel(self):
        self.window.destroy()

    def load_materials(self):
        steels = self.loader.get('steel_grades.json')
        self.material_combo['values'] = list(steels.keys())
        if self.material_combo['values']:
            self.material_combo.current(0)

    def to_float(self, value):
        if not value or not str(value).strip():
            return None
        normalized = str(value).strip().replace(',', '.')
        return float(normalized)

    def on_type_change(self, event):
        # Очищаем старые поля
        for widget in self.param_frame.winfo_children():
            widget.destroy()

        element_type = self.type_var.get()
        if not element_type:
            return

        # Получаем класс и шаблон
        element_class = get_element_class(element_type)
        template = element_class.get_params_template()

        self.entries = {}
        for row, (key, info) in enumerate(template.items()):
            ttk.Label(self.param_frame, text=info["label"]).grid(row=row, column=0, sticky=tk.W, pady=5)
            var = tk.StringVar(value=str(info.get("default", "")))
            self.entries[key] = var
            tk.Entry(self.param_frame, textvariable=var).grid(row=row, column=1, padx=5, pady=5)

    def validate_ref_elements(self, element_type, params):
        if element_type in self.REFERENCE_MAP.keys():
            awaiting_sizes = self.loader.get(self.REFERENCE_MAP.get(element_type))
            input_size = params.get('size')
            if input_size not in awaiting_sizes['weight'].keys():
                messagebox.showerror('Ошибка', f'Типоразмер {input_size} не найден в справочнике!')
                return False
            return True
        else: 
            return True

