import tkinter as tk
from tkinter import ttk, messagebox
from src.domain.construction import Construction
from src.gui.element_editor import ElementEditor

class ConstructionEditor:
    def __init__(self, main_window, root, construction_list, weight_calculator, area_calculator, data_loader, edit_index = None):
        self.main_window = main_window
        self.construction_list = construction_list
        self.weight_calc = weight_calculator
        self.area_calc = area_calculator
        self.data_loader = data_loader
        self.edit_index = edit_index

        self.window = tk.Toplevel(root)
        self.window.title("Создание металлоконструкции")
        self.window.geometry("600x600")

        self.elements = []

        self.create_widgets()

        if self.edit_index is not None:
            construction = self.construction_list[self.edit_index]
            self.name_var.set(construction.name)
            self.count_var.set(construction.quantity)
            self.elements = construction.elements.copy()
            self.refresh_elements_list()

    def create_widgets(self):
        top_frame = ttk.Frame(self.window)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        ttk.Label(top_frame, text="Название:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        tk.Entry(
            top_frame,
            textvariable=self.name_var,
            font=("Arial", 12),
            width=30
        ).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(top_frame, text="Количество:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.count_var = tk.IntVar()
        tk.Entry(
            top_frame,
            textvariable=self.count_var,
            font=("Arial", 12),
            width=30
        ).grid(row=1, column=1, padx=5, pady=5)

        self.listbox = tk.Listbox(self.window, height=20, selectmode=tk.SINGLE)
        self.listbox.pack(fill=tk.X, expand=True, pady=5)

        bottom_frame = ttk.Frame(self.window)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.btn_cancel = ttk.Button(bottom_frame, text="Отмена", command=self.cancel)
        self.btn_cancel.pack(side=tk.RIGHT, padx=5)

        self.btn_save = ttk.Button(bottom_frame, text="Сохранить", command=self.save)
        self.btn_save.pack(side=tk.RIGHT, padx=5)

        center_frame = ttk.Frame(self.window)
        center_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.btn_add = ttk.Button(center_frame, text="Добавить элемент", command=self.on_add)
        self.btn_add.pack(side=tk.LEFT, padx=5)

        self.btn_dell = ttk.Button(center_frame, text="Удалить элемент", command=self.on_dell)
        self.btn_dell.pack(side=tk.LEFT, padx=5)
   
    def on_add(self):
        editor = ElementEditor(
            parent=self.window,
            weight_calculator=self.weight_calc,
            area_calculator=self.area_calc,
            data_loader=self.data_loader,
            existing_element=None
        )
        self.window.wait_window(editor.window)
        if editor.result is not None:
            self.elements.append(editor.result)
            self.refresh_elements_list()


    def on_dell(self):
        selection = self.listbox.curselection()
        if selection:
            self.elements.pop(selection[0])
        else:
            messagebox.showwarning("Info", "Выберете элемент для удаления")
        self.refresh_elements_list()


    def save(self):
        name = self.name_var.get().strip()
        quantity = self.count_var.get()
        if not name:
            messagebox.showerror("Ошибка", "Введите название")
            return 0
        if quantity <= 0:
            messagebox.showerror("Ошибка", "Количество должно быть больше 0")
            return 0
        new_construction = Construction(
            name=name, 
            quantity=quantity, 
            elements=self.elements,
            area_calculator=self.area_calc,
            weight_calculator=self.weight_calc
            )
        
        if self.edit_index is None:
            self.construction_list.append(new_construction)
        else:
            self.construction_list[self.edit_index] = new_construction
        self.window.destroy()
        self.main_window.refresh_list()

    def cancel(self):
        self.window.destroy()

    def refresh_elements_list(self):
        self.listbox.delete(0, tk.END)
        if len(self.elements) == 0:
            pass
        else:
            for element in self.elements:
                display_text = f"{element.element_type}, {element.params} кол-во: {element.quantity} шт"
                self.listbox.insert(tk.END, display_text)