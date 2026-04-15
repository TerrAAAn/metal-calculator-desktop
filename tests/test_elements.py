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
calculator = AreaCalculator()

print(calculator.calculate_area(plate))
print(calculator.calculate_area(circle))
print(calculator.calculate_area(tube))
print(calculator.calculate_area(prof))
print(calculator.calculate_area(angle))
print(calculator.calculate_area(elbow))
print(calculator.calculate_area(reducer))
print(calculator.calculate_area(beam))
print(calculator.calculate_area(channel))
#print(calculate_area(unexpected))

