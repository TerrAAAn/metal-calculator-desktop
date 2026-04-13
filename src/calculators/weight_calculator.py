import json
from pathlib import Path

class WeightCalculator:
    def __init__(self):
        pass

    def load_data(self, file_name):
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent
        filepath = project_root / "data" / file_name
        with open(filepath, 'r', encoding="utf-8") as f:
            return json.load(f)
        
    def get_elbows(self):
        if not hasattr(self, 'elbows_cache'):
            self.elbows_cache = self.load_data('elbows.json')
        return self.elbows_cache

    def calculate_weight(self, element):
        MM3_TO_M3 = 1_000_000_000
        match element.element_type.lower():
            case 'лист':
                length = element.params['length']
                width = element.params['width']
                thickness = element.params['thickness']
                return length * width * thickness * element.material.density * element.quantity / MM3_TO_M3
            case 'круг':
                d = element.params['d']
                length = element.params['length']
                return 3.14 * (d/2)**2 * length * element.material.density * element.quantity / MM3_TO_M3
            case 'труба':
                d = element.params['d']
                length = element.params['length']
                thickness = element.params['thickness']
                s = 3.14 * ((d/2)**2 - ((d - 2*thickness)/2)**2)
                return s * length * element.material.density * element.quantity / MM3_TO_M3
            case 'труба профильная':
                length = element.params['length']
                width = element.params['width']
                height = element.params['height']
                thickness = element.params['thickness']
                s = 2 * thickness * (width + height - 2 * thickness)
                return s * length * element.material.density * element.quantity / MM3_TO_M3
            case 'уголок':
                width_a = element.params['width_a']
                width_b = element.params['width_b']
                thickness = element.params['thickness']
                length = element.params['length']
                s = (width_a + width_b - thickness) * thickness
                return s * length * element.material.density * element.quantity / MM3_TO_M3
            case 'заглушка':
                d = element.params['d']
                thickness = element.params['thickness']
                return (3.14 * (d/2)**2) * thickness * element.material.density * element.quantity / MM3_TO_M3
            case 'отвод':
                size = element.params['size']
                elbows = self.get_elbows()
                mass = elbows['weight'][size]
                return mass * element.quantity
            case _:
                raise ValueError(f"Неизвестный тип элемента: {element.element_type}") 

        
    
    