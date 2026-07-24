from src.domain.base_element import Base_Element

class Reference_element(Base_Element):
    def __init__(self, params, quantity = 1):
        super().__init__(quantity)
        self.params = params

    def get_weight(self):
        return self.get_unit_weight() * self.quantity
    
    def get_painting_area(self):
        return self.get_unit_painting_area() * self.quantity
    
    def get_params_dict(self):
        return {
            'element_name' : self.__class__.__name__,
            'params' : self.params,
            'quantity' : self.quantity,
            'weight' : self.get_weight(),
            'painting_area' : self.get_painting_area()
        }