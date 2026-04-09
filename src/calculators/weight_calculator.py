
def calculate_weight(element):
    if element.element_type.lower() == 'лист':
        length = element.params['length']
        width = element.params['width']
        thickness = element.params['thickness']
        return length * width * thickness * element.material.density * element.quantity / 1000000000
    elif element.element_type.lower() == 'круг':
        d = element.params['d']
        length = element.params['length']
        return 3.14 * (d/2)**2 * length * element.material.density * element.quantity / 1000000000
    elif element.element_type.lower() == 'труба':
        d = element.params['d']
        length = element.params['length']
        thickness = element.params['thickness']
        s = 3.14 * ((d/2)**2 - ((d - 2*thickness)/2)**2)
        return s * length * element.material.density * element.quantity / 1000000000
    elif element.element_type.lower() == 'труба профильная':
        length = element.params['length']
        width = element.params['width']
        height = element.params['height']
        thickness = element.params['thickness']
        s = 2 * thickness * (width + height - 2 * thickness)
        return s * length * element.material.density * element.quantity / 1000000000
    else:
        raise ValueError(f"Неизвестный тип элемента: {element.element_type}") 
    
    