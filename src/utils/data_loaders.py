import json
import sys
from pathlib import Path

class DataLoader:
    def __init__(self):
        self.cache = {}

    def _get_base_path(self):
     
        if getattr(sys, 'frozen', False):
            
            return Path(sys._MEIPASS)
        else:
            
            return Path(__file__).parent.parent.parent

    def load_data(self, file_name):
        base_path = self._get_base_path()
        filepath = base_path / "data" / file_name
        
        if not filepath.exists():
            raise FileNotFoundError(f"Файл не найден: {filepath}")
        
        with open(filepath, 'r', encoding="utf-8") as f:
            return json.load(f)
        
    def get(self, elements_name):
        if elements_name not in self.cache:
            self.cache[elements_name] = self.load_data(elements_name)
        return self.cache[elements_name]

def get_save_dir():
    # Возвращение папки для сохранений
    if getattr(sys, 'frozen', False):
        base = Path(sys.executable).parent
    else:
        base = Path(__file__).parent.parent.parent
    save_dir = base / "saves"
    save_dir.mkdir(exist_ok=True)
    return save_dir