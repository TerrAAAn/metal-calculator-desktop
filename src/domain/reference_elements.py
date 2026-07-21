from src.domain.reference_element import Reference_element
from src.utils.data_loaders import DataLoader

class Beam(Reference_element):
    def __init__(self, params, quantity=1):
        super().__init__(params, quantity)
        self.loader = DataLoader()

    @staticmethod
    def get_params_template():
        return {
            'size' : {"label": "Типоразмер", "default": '10б1'},
            'length' : {"label": "Длина, м", "default": 1}
        }
    
    def get_unit_weight(self):
        weight_data = self.loader.get('beams.json')['weight']
        return weight_data[self.params['size']] * self.params['length']
        
    def get_unit_painting_area(self):
        area_data = self.loader.get('beams.json')['area']
        return area_data[self.params['size']] * self.params['length']
    
class Channel(Reference_element):
    def __init__(self, params, quantity=1):
        super().__init__(params, quantity)
        self.loader = DataLoader()

    @staticmethod
    def get_params_template():
        return {
            'size' : {"label": "Типоразмер", "default": '5у'},
            'length' : {"label": "Длина, м", "default": 1}
        }
    
    def get_unit_weight(self):
        weight_data = self.loader.get('channels.json')['weight']
        return weight_data[self.params['size']] * self.params['length']
        
    def get_unit_painting_area(self):
        area_data = self.loader.get('channels.json')['area']
        return area_data[self.params['size']] * self.params['length']
    
class Elbow(Reference_element):
    def __init__(self, params, quantity=1):
        super().__init__(params, quantity)
        self.loader = DataLoader()

    @staticmethod
    def get_params_template():
        return {
            'size' : {"label": "Типоразмер", "default": '57x3,5'}
        }
    
    def get_unit_weight(self):
        weight_data = self.loader.get('elbows.json')['weight']
        return weight_data[self.params['size']] 
        
    def get_unit_painting_area(self):
        area_data = self.loader.get('elbows.json')['area']
        return area_data[self.params['size']]

class Reducer(Reference_element):
    def __init__(self, params, quantity=1):
        super().__init__(params, quantity)
        self.loader = DataLoader()
    
    @staticmethod
    def get_params_template():
        return {
            'size' : {'label': 'Типоразмер', 'default': '57x32'}
        }
    
    def get_unit_weight(self):
        weight_data = self.loader.get('reducers.json')['weight']
        return weight_data[self.params['size']] 
        
    def get_unit_painting_area(self):
        area_data = self.loader.get('reducers.json')['area']
        return area_data[self.params['size']]


    
