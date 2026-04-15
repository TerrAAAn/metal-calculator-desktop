from src.utils.data_loaders import DataLoader

class AreaCalculator:
    def __init__(self):
        self.loader = DataLoader()
    
    def calculate_area(self, element):
        MM2_TO_M2 = 1_000_000
        match element.element_type.lower():
            case 'лист':
                length = element.params['length']
                width = element.params['width']
                return length * width * element.quantity / MM2_TO_M2
            case 'круг' | 'труба':
                d = element.params['d']
                length = element.params['length']
                return 3.14 * d * length * element.quantity / MM2_TO_M2
            case 'труба профильная':
                length = element.params['length']
                width = element.params['width']
                height = element.params['height']
                return 2 * (width + height) * length * element.quantity / MM2_TO_M2
            case 'уголок':
                width_a = element.params['width_a']
                width_b = element.params['width_b']
                length = element.params['length']
                return 2 * (width_a + width_b) * length * element.quantity / MM2_TO_M2
            case 'заглушка':
                d = element.params['d']
                return 3.14 * ((d/2)**2) * element.quantity / MM2_TO_M2
            case 'отвод':
                size = element.params['size']
                elbows = self.loader.get('elbows.json')
                area = elbows['area'][size]
                return area * element.quantity 
            case 'переход':
                size = element.params['size']
                reducers = self.loader.get('reducers.json')
                area = reducers['area'][size]
                return area * element.quantity
            case 'швеллер':
                size = element.params['size']
                channels = self.loader.get('channels.json')
                area = channels['area'][size]
                length = element.params['length']
                return area * element.quantity * length 
            case 'балка' | 'двутавр':
                size = element.params['size']
                beams = self.loader.get('beams.json')
                area = beams['area'][size]
                length = element.params['length']
                return area * element.quantity * length 
            case _: 
                raise ValueError(f"Неизвестный тип элемента: {element.element_type}")
    
    
        
    