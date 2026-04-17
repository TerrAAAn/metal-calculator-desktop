import tkinter as tk
from tkinter import ttk, messagebox
from src.domain.construction import Construction

class ConstructionEditor:
    def __init__(self, parent, construction_list, weight_calculator, area_calculator, data_loader, edit_index = None):
        self.window = tk.Toplevel(parent)
        self.window.title("Создание металлоконструкции")
        self.window.geometry("600x400")

        label = ttk.label(self.window, text="Окно редактора конструкций")
        label.pack(pady=50)
        
    def save(self):
        pass

    def cancel(self):
        pass