import tkinter as tk
from src.gui.main_window import Main_window

def main():
    root = tk.Tk()
    app = Main_window(root)
    app.refresh_constructions_listbox()
    root.mainloop()

if __name__ == "__main__":
    main()
