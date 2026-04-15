
class Construction:
    def __init__(self, name, quantity, elements, area_calculator, weight_calculator,):
        if quantity <= 0:
            raise ValueError('Количество элемента должно быть > 0')
        if not isinstance(elements, list) and not isinstance(elements, tuple):
            raise ValueError('elements должен быть списком или кортежем')
        self.name = name
        self.quantity = quantity
        self.elements = elements
        self.area_calc = area_calculator
        self.weight_calc = weight_calculator
        
    def total_weight(self):
        result = 0
        for element in self.elements:
            result += self.weight_calc.calculate_weight(element)
        return result
    
    def total_area(self):
        result = 0
        for element in self.elements:
            result += self.area_calc.calculate_area(element)
        return result

    def __repr__(self):
        lines = []
        lines.append(f'===== {self.name} - Количество: {self.quantity} =====')
        lines.append('')
        for element in self.elements:
            lines.append(str(element))
        lines.append(f'Масса одной конструкции: {self.total_weight()} кг')
        lines.append(f'Площадь одной конструкции: {self.total_area()} м²')
        lines.append('')
        lines.append(f'Общая масса: {self.total_weight() * self.quantity} кг')
        lines.append(f'Общая площадь: {self.total_area() * self.quantity} м²')
        return '\n'.join(lines)