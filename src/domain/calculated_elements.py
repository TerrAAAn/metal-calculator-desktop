from src.domain.calculated_element import Calculated_element
PI = 3.14159

class Pipe(Calculated_element):
    def __init__(self, density, params, quantity=1):
        super().__init__(density, params, quantity)

    @staticmethod
    def get_params_template():
        return {
            'diameter' : {"label": "Диаметр (мм)", "default": 57},
            'thickness' : {"label": "Толщина стенки (мм)", "default": 3.5},
            'length' : {"label" : "Длина (м)", "default" : 1}
        }
    
    def get_volume(self):
        d = self.params['diameter'] / 1000
        t = self.params['thickness'] / 1000
        d_inner = d - 2 * t
        return PI / 4 * (d**2 - d_inner**2) * self.params['length']
    
    def get_surface_area(self):
        d = self.params['diameter'] / 1000
        return PI * d * self.params['length']
    
class Round_bar(Calculated_element):
    def __init__(self, density, params, quantity=1):
        super().__init__(density, params, quantity)

    @staticmethod
    def get_params_template():
        return {
            'diameter' : {"label": "Диаметр (мм)", "default": 16},
            'length' : {"label" : "Длина (м)", "default" : 1}
        }
    
    def get_volume(self):
        d = self.params['diameter'] / 1000
        cross_section_area = PI * (d**2) / 4
        return  cross_section_area * self.params['length'] 
    
    def get_surface_area(self):
        d = self.params['diameter'] / 1000
        return PI * d * self.params['length']
    
class Sheet(Calculated_element):
    def __init__(self, density, params, quantity=1):
        super().__init__(density, params, quantity)
    
    @staticmethod
    def get_params_template():
        return {
            'length' : {"label" : "Длина (мм)", "default" : 1000},
            'width' : {"label" : "Ширина (мм)", "default" : 1000},
            'thickness' : {"label" : "Толщина (мм)", "default" : 4}
        }
    
    def get_volume(self):
        l = self.params['length'] / 1000
        w = self.params['width'] / 1000
        t = self.params['thickness'] / 1000
        return l * w * t
    
    def get_surface_area(self):
        l = self.params['length'] / 1000
        w = self.params['width'] / 1000
        return l * w
    
class Strip(Calculated_element):
    def __init__(self, density, params, quantity=1):
        super().__init__(density, params, quantity)

    @staticmethod
    def get_params_template():
        return {
            'length' : {"label" : "Длина (м)", "default" : 1},
            'width' : {"label" : "Ширина (мм)", "default" : 1000},
            'thickness' : {"label" : "Толщина (мм)", "default" : 4}
        }
    
    def get_volume(self):
        l = self.params['length'] 
        w = self.params['width'] / 1000
        t = self.params['thickness'] / 1000
        return l * w * t
    
    def get_surface_area(self):
        l = self.params['length'] 
        w = self.params['width'] / 1000
        return l * w
    
class Profile_pipe(Calculated_element):
    def __init__(self, density, params, quantity=1):
        super().__init__(density, params, quantity)

    @staticmethod
    def get_params_template():
        return {
            'width' : {"label" : "Ширина (мм)", "default" : 100},
            'height' : {"label" : "Высота (мм)", "default" : 100},
            'thickness' : {"label" : "Толщина (мм)", "default" : 3},
            'length' : {"label" : "Длина (м)", "default" : 1}       
        }
    
    def get_volume(self):
        l = self.params['length'] 
        w = self.params['width'] / 1000
        h = self.params['height'] / 1000
        t = self.params['thickness'] / 1000
        Vouter = w * h * l
        Vinner = (w - 2*t) * (h - 2*t) * l
        return Vouter - Vinner
    
    def get_surface_area(self):
        l = self.params['length'] 
        w = self.params['width'] / 1000
        h = self.params['height'] / 1000
        return 2*(w+h) * l
    
class Angle(Calculated_element):
    def __init__(self, density, params, quantity=1):
        super().__init__(density, params, quantity)

    @staticmethod
    def get_params_template():
        return {
            'width_a' : {"label" : "Ширина полки 1 (мм)", "default" : 40},
            'width_b' : {"label" : "Ширина полки 2 (мм)", "default" : 40},
            'thickness' : {"label" : "Толщина (мм)", "default" : 3},
            'length' : {"label" : "Длина (м)", "default" : 1}
        }
    
    def get_volume(self):
        w_a = self.params['width_a'] / 1000
        w_b = self.params['width_b'] / 1000
        l = self.params['length']
        t = self.params['thickness'] / 1000
        return ((w_a * t) + ((w_b - t) * t)) * l
    
    def get_surface_area(self):
        w_a = self.params['width_a'] / 1000
        w_b = self.params['width_b'] / 1000
        l = self.params['length']
        return 2*(w_a + w_b) * l
    
class Cap(Calculated_element):
    def __init__(self, density, params, quantity=1):
        super().__init__(density, params, quantity)

    @staticmethod
    def get_params_template():
        return {
            'diameter' : {"label": "Диаметр (мм)", "default": 57},
            'thickness' : {"label": "Толщина стенки (мм)", "default": 3.5}
        }
    
    def get_volume(self):
        d = self.params['diameter'] / 1000
        t = self.params['thickness'] / 1000
        return PI * t * (d/2)**2
    
    def get_surface_area(self):
        d = self.params['diameter'] / 1000
        return PI * (d/2)**2