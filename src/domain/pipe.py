from src.domain.calculated_element import Calculated_element
PI = 3.14159
class Pipe(Calculated_element):
    def __init__(self, length, density, params, quantity=1):
        super().__init__(density, params, quantity)
        self.length = length

    @staticmethod
    def get_params_template():
        return {
            'diameter' : {"label": "Диаметр (мм)", "default": 57},
            'wall_thickness' : {"label": "Толщина стенки (мм)", "default": 3.5}
        }
    
    def get_cross_section_area(self):
        d = self.params['diameter'] / 1000
        t = self.params['wall_thickness'] / 1000
        d_inner = d - 2 * t
        return PI / 4 * (d**2 - d_inner**2) * self.length
    
    def get_surface_area(self):
        d = self.params['diameter'] / 1000
        return PI * d * self.length * self.quantity
    
