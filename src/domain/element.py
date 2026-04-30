
class Element:
    def __init__(self, params, quantity, material, element_type):
        if quantity <= 0:
            raise ValueError('Количество элемента должно быть > 0')
        if not isinstance(params, dict):
            raise ValueError('params должен быть словарём')
        self.params = params
        self.quantity = quantity
        self.material = material
        self.element_type = element_type
    
    def __repr__(self):   
        return f'- {self.element_type} : {self.material.name}, количество: {self.quantity}, параметры: {self.params}'

    # ["лист", "круг", "труба", "труба профильная", "уголок", "отвод", "переход", "балка", "швеллер", "заглушка"]
    def get_display_string(self):
        match self.element_type:
            case "лист":
                return f"{self.params['length']}x{self.params['width']}, толщ. {self.params['thickness']}"
            case "круг":
                return f"{self.params['d']}, L={self.params['length']/1000}м"
            case "труба":
                return f"{self.params['d']}x{self.params['thickness']}, L={self.params['length']/1000}м"
            case "труба профильная":
                return f"{self.params['width']}x{self.params['height']} толщ. {self.params['thickness']},  L={self.params['length']/1000}м"
            case 'уголок':
                return f"{self.params['width_a']}x{self.params['width_b']} толщ. {self.params['thickness']},  L={self.params['length']/1000}м"
            case 'отвод' | 'переход':
                return f"{self.params['size']}"
            case 'заглушка':
                return f"{self.params['d']}x{self.params['thickness']}"
            case 'балка' | 'швеллер':
                return f"{self.params['size']}, L={self.params['length']}м"
            case _:
                return "Unknown params"   