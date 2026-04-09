
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

        