from src.domain.base_element import Base_Element

class Calculated_element(Base_Element):
    def __init__(self, density, params, quantity = 1):
        super().__init__(quantity)
        self.density = density
        self.params = params

    def get_weight(self):
        return self.get_cross_section_area() * self.density * self.quantity
    
    def get_painting_area(self):
        return self.get_surface_area() * self.quantity

