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
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.create_widgets()

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
        list_frame.pack(fill=tk.X, expand=True, padx=10, pady=10)
        self.listbox = tk.Listbox(
            list_frame,
            height=15,
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#1e293b",
            selectbackground="#3b82f6",
            selectforeground="#ffffff",
            relief=tk.FLAT,
            highlightthickness=0
        )
        self.listbox.pack(fill=tk.BOTH, expand=True)

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
        self.listbox.delete(0, tk.END)
        if len(self.project.construction_list) != 0:
            for construction in self.project.construction_list:
                self.listbox.insert(tk.END, construction.get_display_string()) 

    def on_add(self):
        Construction_Editor(
            root= self.root,
            main_window=self,
            project= self.project,
            edit_index= None
        )

    def on_edit(self):
        selection = self.listbox.curselection()
        if selection:
            Construction_Editor(
                root= self.root,
                main_window=self,
                project= self.project,
                edit_index= selection[0]
                )
        else:
            messagebox.showerror('Элемент для редактирования не выбран!')
        self.refresh_constructions_listbox()

    def on_delete(self):
        selection = self.listbox.curselection()
        if selection:
            self.project.remove_construction(selection[0])
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
