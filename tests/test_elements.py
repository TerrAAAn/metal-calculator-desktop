from src.domain.material import Material
from src.domain.element import Element
from src.calculators.weight_calculator import WeightCalculator

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

unexpected = Element(
    element_type='слесарь',
    params={'mass' : 80,  'width_b' : 50, 'thickness' :5, 'length' : 6000},
    quantity=1,
    material=steel
)
calculator = WeightCalculator()

print(calculator.calculate_weight(plate))
print(calculator.calculate_weight(circle))
print(calculator.calculate_weight(tube))
print(calculator.calculate_weight(prof))
print(calculator.calculate_weight(angle))
print(calculator.calculate_weight(elbow))
#print(calculate_weight(unexpected))

