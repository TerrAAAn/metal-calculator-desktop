import json
from pathlib import Path

class DataLoader:
    def __init__(self):
        self.cache = {}
        
    def load_data(self, file_name):
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent
        filepath = project_root / "data" / file_name
        with open(filepath, 'r', encoding="utf-8") as f:
            return json.load(f)
        
    def get(self, elements_name):
        if elements_name not in self.cache:
            self.cache[elements_name] = self.load_data(elements_name)
        return self.cache[elements_name]