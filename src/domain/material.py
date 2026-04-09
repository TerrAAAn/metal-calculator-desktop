import json
from pathlib import Path

class Material:
    def __init__(self, name, density):
        if not isinstance(name, str):
            raise ValueError('Поле имя имеет строковый тип')
        if len(name.strip()) == 0:
            raise ValueError('Ошибка - пустая строка')
        if not isinstance(density, (int, float)):
            raise ValueError('Плотность должна быть числом')
        if density <= 0 or density >= 30000:
            raise ValueError('Некорректная плотность')
        self.name = name
        self.density = density

    @staticmethod
    def load_from_json():
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent
        filepath = project_root / "data" / "steel_grades.json"
        d = {}
        with open(filepath, 'r', encoding="utf-8") as f:
            data = json.load(f)
        for name, density in data.items():
            d.update({name : Material(name, density)})
        return d
        
