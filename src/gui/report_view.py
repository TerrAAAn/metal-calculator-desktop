import tkinter as tk
from tkinter import ttk, messagebox

class ReportView:
    def __init__(self, main_window, construction_list, weight_calculator, area_calculator, data_loader,):
        self.main_window = main_window
        self.construction_list = construction_list
        self.weight_calc = weight_calculator
        self.area_calc = area_calculator
        self.data_loader = data_loader

        self.window = tk.Toplevel(main_window)
        self.window.title("Отчет")
        self.window.geometry("600x600")

        text_widget = tk.Text(
            master=  self.window,
            height= 20,
            width= 70,
            font=("Arial", 10),
            wrap=tk.WORD
        )
        text_widget.pack(pady=10)


        for construction in self.construction_list:
            weight = round(construction.total_weight(), 2)
            area = round(construction.total_area(),2)
            construction_info = f'{construction.name}: Общий вес:{weight} кг. Общая площадь: {area} м2\n'
            text_widget.insert(tk.END, construction_info)

        self.btn_cancel = ttk.Button(self.window, text="Закрыть", command=self.close)
        self.btn_cancel.pack(side=tk.BOTTOM, padx=5)

    def close(self):
        self.window.destroy()