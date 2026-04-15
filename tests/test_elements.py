from src.domain.material import Material
from src.domain.element import Element
from src.calculators.weight_calculator import WeightCalculator
from src.calculators.area_calculator import AreaCalculator

materials = Material.load_from_json()

steel = materials["Ст3"]

plate = Element(
    params={'length' : 2000, 'width' : 1000, 'thickness' : 5},
    quantity=1,
    material=steel,
    element_type='Лист'
)

circle = Element(
    params={'d' : 50, 'length' : 1000,},
    quantity=1,
    material=steel,
    element_type='Круг'
)

tube = Element(
    params={'d' : 57, 'thickness' : 3.5, 'length' : 6000,},
    quantity=1,
    material=steel,
    element_type='Труба'
)


prof = Element(
    params={'width' : 40, 'height' : 20, 'thickness' :2, 'length' : 6000},
    quantity=1,
    material=steel,
    element_type='труба профильная'
)

angle = Element(
    element_type='уголок',
    params={'width_a' : 40,  'width_b' : 50, 'thickness' :5, 'length' : 6000},
    quantity=4,
    material=steel
)

elbow = Element(
    element_type='отвод',
    params={'size' : "32x2,5"},
    quantity=2,
    material=steel
)

reducer = Element(
    element_type='переход',
    params={'size' : "76x57"},
    quantity=2,
    material=steel
)

beam = Element(
    element_type='балка',
    params={'size' : "40", 'length' : 1},
    quantity=1,
    material=steel
)

channel = Element(
    element_type='швеллер',
    params={'size' :"5у", 'length' : 1},
    quantity=1,
    material=steel
)

unexpected = Element(
    element_type='слесарь',
    params={'mass' : 80,  'width_b' : 50, 'thickness' :5, 'length' : 6000},
    quantity=1,
    material=steel
)

area_calculator = AreaCalculator()
weight_calculator = WeightCalculator()


print('Площади:')
print(area_calculator.calculate_area(plate))
print(area_calculator.calculate_area(circle))
print(area_calculator.calculate_area(tube))
print(area_calculator.calculate_area(prof))
print(area_calculator.calculate_area(angle))
print(area_calculator.calculate_area(elbow))
print(area_calculator.calculate_area(reducer))
print(area_calculator.calculate_area(beam))
print(area_calculator.calculate_area(channel))
print('Вес:')
print(weight_calculator.calculate_weight(plate))
print(weight_calculator.calculate_weight(circle))
print(weight_calculator.calculate_weight(tube))
print(weight_calculator.calculate_weight(prof))
print(weight_calculator.calculate_weight(angle))
print(weight_calculator.calculate_weight(elbow))
print(weight_calculator.calculate_weight(reducer))
print(weight_calculator.calculate_weight(beam))
print(weight_calculator.calculate_weight(channel))
#print(weight_calculator.calculate_weight(unexpected))



