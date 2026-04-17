import tkinter as tk
from tkinter import ttk, messagebox
from src.gui.construction_editor import ConstructionEditor

class MainWindow:
    def __init__(self, root, weight_calculator, area_calculator, data_loader):
        self.root = root
        self.weight_calculator = weight_calculator
        self.area_calculator = area_calculator
        self.data_loader = data_loader
        
        self.constructions = []

        self.root.title("Калькулятор металлоконструкций")
        self.root.geometry("600x400")

        self.create_widgets()
        self.refresh_list()

    def create_widgets(self):
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(list_frame, text="Список металлоконструкций", font=("Arial", 12)).pack(anchor=tk.NW)
        # Список элементов
        self.listbox = tk.Listbox(list_frame, height=15, selectmode=tk.SINGLE)
        self.listbox.pack(fill=tk.X, expand=True, pady=5)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        self.btn_add = ttk.Button(button_frame, text="Добавить", command=self.on_add)
        self.btn_add.pack(side=tk.LEFT, padx=5)

        self.btn_edit = ttk.Button(button_frame, text="Редактировать", command=self.on_edit)
        self.btn_edit.pack(side=tk.LEFT, padx=5)
        
        self.btn_delete = ttk.Button(button_frame, text="Удалить", command=self.on_delete)
        self.btn_delete.pack(side=tk.LEFT, padx=5)

        self.btn_report = ttk.Button(button_frame, text="Расчёт", command=self.on_report)
        self.btn_report.pack(side=tk.RIGHT, padx=5)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        if len(self.constructions) == 0:
            pass
        else:
            for construction in self.constructions:
                display_text = f"{construction.name} (кол-во: {construction.quantity} шт)"
                self.listbox.insert(tk.END, display_text)
        

    def on_add(self):
        ConstructionEditor(
            main_window=self,
            root=self.root, 
            construction_list=self.constructions, 
            weight_calculator=self.weight_calculator,
            area_calculator=self.area_calculator,
            data_loader=self.data_loader,
            edit_index=None
            )
        
    def on_delete(self):
        selection = self.listbox.curselection()
        if selection:
            self.constructions.pop(selection[0])
        else:
            messagebox.showwarning("Info", "Выберете элемент для удаления")
        self.refresh_list()

    def on_edit(self):
        selection = self.listbox.curselection()
        if selection:
            ConstructionEditor(
                main_window=self,
                root=self.root,  
                construction_list=self.constructions, 
                weight_calculator=self.weight_calculator,
                area_calculator=self.area_calculator,
                data_loader=self.data_loader,
                edit_index=selection[0]
                )
        else:
            messagebox.showwarning("Info", "Выберете элемент для редактирования")
        self.refresh_list()

    def on_report(self):
        messagebox.showinfo("Info", "В разработке...")