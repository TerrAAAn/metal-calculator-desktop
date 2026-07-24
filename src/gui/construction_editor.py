import tkinter as tk
from tkinter import ttk, messagebox
from src.domain.construction import Construction
from src.gui.element_editor import Element_editor

class Construction_Editor:
    def __init__(self, root, main_window, project, edit_index = None):
            self.root = root
            self.main_window = main_window
            self.project = project
            self.edit_index = edit_index
            self.window = tk.Toplevel(root)
            self.window.title("Создание / редактирование конструкции")
            self.window.geometry("800x600")
            self.window.resizable(False, False)
            self.construction = Construction()

            self.create_widgets()
            # редактирование существующей конструкции -> 
            # если при вызове окна была выбрана конструкция в листе, то
            # Получить из текущего проекта конструкцию по индексу
            # Обновить нужные параметры
            # Заменить выбранную конструкцию на новую по нажатии кнопки сохранить
            # Вернуться на мейн в любом случае при нажатии кнопки

            if self.edit_index is not None:
                existing = self.project.get_construction(edit_index)
                self.construction.name = existing.name
                self.construction.quantity = existing.quantity
                self.construction.elements_list = existing.get_elements_list().copy()

            self.entries["name"].set(self.construction.name)
            self.entries["quantity"].set(str(self.construction.quantity))     
            self.refresh_elements_listbox()
            

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
        
        # Верхний тулбар - кнопки "сохранить изменения", "отменить изменения"
        toolbar_frame = ttk.Frame(self.window)
        toolbar_frame.pack(fill=tk.X, expand=True, padx=15, pady=10)
        
        self.btn_save = ttk.Button(toolbar_frame, text="Сохранить", command=self.on_save, style="Accent.TButton")
        self.btn_save.pack(side=tk.LEFT, padx=5)
                
        self.btn_cancel = ttk.Button(toolbar_frame, text="Отмена", command=self.on_cancel, style="Del.TButton")
        self.btn_cancel.pack(side=tk.LEFT, padx=5)

        ttk.Separator(self.window, orient='horizontal').pack(fill=tk.X, padx=15, pady=5)

        top_frame = ttk.Frame(self.window)
        top_frame.pack(fill=tk.X, expand=True, padx=15, pady=10)

        # Формы ввода названия и количества конструкциий
        self.create_param_fields(top_frame)

        #Список элементов выбранной (добавляемой конструкции)
        ttk.Label(self.window, text= "Элементы металлоконструкции", style="Header.TLabel").pack(anchor=tk.W, padx=15, pady=(5, 5)) 
        list_frame = ttk.Frame(self.window)
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
        
        ttk.Separator(self.window, orient='horizontal').pack(fill=tk.X, padx=15, pady=5)

        # Кнопки управления списком элементов:
        buttons_frame = ttk.Frame(self.window)
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.btn_add = ttk.Button(buttons_frame, text="Добавить элемент", command=self.on_add, style="Accent.TButton")
        self.btn_add.pack(side=tk.LEFT, padx=5)
        
        self.btn_edit = ttk.Button(buttons_frame, text="Редактировать элемент", command=self.on_edit, style="Redo.TButton")
        self.btn_edit.pack(side=tk.LEFT, padx=5)
                
        self.btn_delete = ttk.Button(buttons_frame, text="Удалить элемент", command=self.on_delete, style="Del.TButton")
        self.btn_delete.pack(side=tk.LEFT, padx=5)

    def on_save(self):
        # Чтение полей и валидация
        name = self.entries["name"].get().strip()
        if not name:
            messagebox.showerror("Ошибка", "Введите название")
            return

        try:
            quantity = int(self.entries["quantity"].get())
        except ValueError:
            messagebox.showerror("Ошибка", "Количество должно быть числом")
            return

        if quantity <= 0:
            messagebox.showerror("Ошибка", "Количество должно быть больше 0")
            return

        self.construction.name = name
        self.construction.quantity = quantity

        # Добавление НОВОЙ конструкции
        if self.edit_index is None:
            self.project.add_construction(self.construction)
        else:
        # Обновление существующей:
            self.project.replace_construction(self.edit_index, self.construction)

        self.window.destroy()  
        self.main_window.refresh_constructions_listbox()

    def on_cancel(self):
        self.window.destroy()

    def on_add(self):
        Element_editor(
            root = self,
            main_window=self.window,
            construction=self.construction,
            edit_index=None
        )

    def on_edit(self):
        selection = self.listbox.curselection()
        if selection:
            Element_editor(
                root = self,
                main_window=self.window,
                construction=self.construction,
                edit_index=selection[0]
            )

    def on_delete(self):
        selection = self.listbox.curselection()
        if selection:
            self.construction.remove_element(selection[0])
            self.refresh_elements_listbox()

    def refresh_elements_listbox(self):
        self.listbox.delete(0, tk.END)
        if self.construction.elements_list:
            for element in self.construction.elements_list:
                self.listbox.insert(tk.END, element.get_display_string())

    def create_param_fields(self, parent):
        template = Construction.get_params_template()
        self.entries = {}
        for row, (key, info) in enumerate(template.items()):
            ttk.Label(parent, text=info["label"]).grid(row=row, column=0, sticky=tk.W, pady=5)
            var = tk.StringVar(value=str(info.get("default", "")))
            self.entries[key] = var
            tk.Entry(parent, textvariable=var).grid(row=row, column=1, padx=5, pady=5)
