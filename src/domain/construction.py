
class Construction:
    def __init__(self, name = 'Металлоконструкция', quantity = 1):
        self.name = name
        self.quantity = quantity
        self.elements_list = []

    @staticmethod
    def get_params_template():
        return {
            'name' : {"label": "Название металлоконструкции", "default": 'Металлоконструкция'},
            'quantity' : {"label" : "Количество металлоконструкций", "default" : 1}
        }
    
    def add_element(self, element):
        self.elements_list.append(element)

    def remove_element(self, index: int):
        if index >= 0 and index < len(self.elements_list):
            return self.elements_list.pop(index)
        else:
            raise IndexError('Индекс вне диапазона')
    
    def get_total_weight(self):
        return sum(element.get_weight() for element in self.elements_list)
    
    def get_total_painting_area(self):
        return sum(element.get_painting_area() for element in self.elements_list)
    
    def get_elements_list(self):
        return self.elements_list.copy()
    
    def clear_elements_list(self):
        self.elements_list.clear()

    def replace_element(self, index, new_element):
        if index >= 0 and index < len(self.elements_list):
            self.elements_list[index] = new_element
        else:
            raise IndexError('Индекс вне диапазона')
    
    def update_element_param(self, index : int, new_params_dict: dict, new_quantity: int):
        if index < 0 or index >= len(self.elements_list):
            raise IndexError("Индекс вне диапазона")
        
        element = self.get_elements_list()[index]

        if hasattr(element, 'params'):   
            element.params.update(new_params_dict)
        else:
            raise AttributeError(f'Элемент {element} не имеет атрибута параметры')
        if hasattr(element, 'quantity'):
            element.quantity = new_quantity
        else:
            raise AttributeError(f'Элемент {element} не имеет атрибута количество')
        
    def get_display_string(self):
        return f'{self.name} - {self.quantity} шт.'
    
    