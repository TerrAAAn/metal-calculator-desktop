import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from src.domain.project import Project
from src.gui.construction_editor import Construction_Editor
from src.utils.data_loaders import get_save_dir

class Main_window:
    def __init__(self, root):
        self.root = root
        self.project = Project('Новый проект')
        self.root.title("Калькулятор металлоконструкций")
        self.root.geometry("1250x600")
        self.root.resizable(False, False)

        self.create_widgets()
        self.refresh_constructions_listbox()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="#1e3a8a")  # тёмно-синий
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), foreground="#ffffff", background="#2563eb")  
        style.map("Accent.TButton", background=[("active", "#1d4ed8")])
        style.configure("Del.TButton", font=("Segoe UI", 10, "bold"), foreground="#ffffff", background="#be2828")  
        style.map("Del.TButton", background=[("active", "#9e2b2b")])
        style.configure("Redo.TButton", font=("Segoe UI", 10, "bold"), foreground="#ffffff", background="#acbe28")  
        style.map("Redo.TButton", background=[("active", "#808b2e")])
        style.configure("Treeview", 
            background="#f8fafc",
            foreground="#1e293b",
            rowheight=25,
            fieldbackground="#f8fafc",
            borderwidth=1,
            relief="solid"
        )
        style.configure("Treeview.Heading", 
            font=("Segoe UI", 10, "bold"),
            foreground="#1e3a8a",
            background="#e2e8f0",
            relief="solid",
            borderwidth=1
        )
        style.map("Treeview", 
            background=[("selected", "#3b82f6")],
            foreground=[("selected", "#ffffff")]
        )
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        # Верхний тулбар
        toolbar_frame = ttk.Frame(self.root)
        toolbar_frame.pack(fill=tk.X, expand=True, padx=15, pady=10)

        self.btn_save = ttk.Button(toolbar_frame, text="Сохранить текущий проект", command=self.on_save)
        self.btn_save.pack(side=tk.LEFT, padx=5)
        
        self.btn_load = ttk.Button(toolbar_frame, text="Загрузить проект", command=self.on_load)
        self.btn_load.pack(side=tk.LEFT, padx=5)

        ttk.Separator(self.root, orient='horizontal').pack(fill=tk.X, padx=15, pady=5)

        # Список
        ttk.Label(self.root, text="Список металлоконструкций", style="Header.TLabel").pack(anchor=tk.W, padx=15, pady=(5, 5)) 
        list_frame = ttk.Frame(self.root)
        columns = ("№", "Название", "Кол-во", "Вес, кг", "Площадь, м²", "Общий вес, кг", "Общая площадь, м²")
        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            height=15
        )

        # Заголовки
        self.tree.heading("№", text="№")
        self.tree.heading("Название", text="Название")
        self.tree.heading("Кол-во", text="Кол-во")
        self.tree.heading("Вес, кг", text="Вес, кг")
        self.tree.heading("Площадь, м²", text="Площадь, м²")
        self.tree.heading("Общий вес, кг", text="Общий вес, кг")
        self.tree.heading("Общая площадь, м²", text="Общая площадь, м²")

        # Ширина и выравнивание
        self.tree.column("№", width=20, anchor="center")
        self.tree.column("Название", width=250, anchor="w")
        self.tree.column("Кол-во", width=40, anchor="center")
        self.tree.column("Вес, кг", width=100, anchor="center")
        self.tree.column("Площадь, м²", width=100, anchor="center")
        self.tree.column("Общий вес, кг", width=100, anchor="center")
        self.tree.column("Общая площадь, м²", width=100, anchor="center")

        # Упаковка
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.pack(fill=tk.BOTH, expand=True)

        ttk.Separator(self.root, orient='horizontal').pack(fill=tk.X, padx=15, pady=5)

        # Кнопки управления
        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.btn_add = ttk.Button(buttons_frame, text="Добавить", command=self.on_add, style="Accent.TButton")
        self.btn_add.pack(side=tk.LEFT, padx=5)

        self.btn_edit = ttk.Button(buttons_frame, text="Редактировать", command=self.on_edit, style="Redo.TButton")
        self.btn_edit.pack(side=tk.LEFT, padx=5)
        
        self.btn_delete = ttk.Button(buttons_frame, text="Удалить", command=self.on_delete, style="Del.TButton")
        self.btn_delete.pack(side=tk.LEFT, padx=5)

    def refresh_constructions_listbox(self):

        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for i, construction in enumerate(self.project.construction_list, start=1):
            self.tree.insert(
                "",
                tk.END,
                values=(
                    i,
                    construction.name,
                    construction.quantity,
                    f"{construction.get_total_weight():.2f}",
                    f"{construction.get_total_painting_area():.2f}",
                    f"{construction.get_total_weight()*construction.quantity:.2f}",
                    f"{construction.get_total_painting_area()*construction.quantity:.2f}"
                )
            )

    def on_add(self):
        Construction_Editor(
            root= self.root,
            main_window=self,
            project= self.project,
            edit_index= None
        )

    def on_edit(self):
        selected = self.tree.selection()
        if selected:
            index = self.tree.index(selected[0])
            Construction_Editor(
                root= self.root,
                main_window=self,
                project= self.project,
                edit_index= index
                )
        else:
            messagebox.showerror('Элемент для редактирования не выбран!')

    def on_delete(self):
        selected = self.tree.selection()
        if selected:
            index = self.tree.index(selected[0])
            self.project.remove_construction(index)
            self.refresh_constructions_listbox()

    def on_save(self):
        save_dir = get_save_dir()
        filepath = filedialog.asksaveasfilename(
            title="Сохранить проект",
            initialdir=save_dir,
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if not filepath:
            return

        try:
            data = self.project.to_dict()
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Успех", f"Проект сохранён:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить проект:\n{e}")

    def on_load(self):
        save_dir = get_save_dir()
        filepath = filedialog.askopenfilename(
            title="Загрузить проект",
            initialdir=save_dir,
            filetypes=[("JSON files", "*.json")]
        )
        if not filepath:
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.project = Project.from_dict(data)
            self.refresh_constructions_listbox()
            messagebox.showinfo("Успех", f"Проект загружен:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить проект:\n{e}")
