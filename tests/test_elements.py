from src.domain.material import Material
from src.domain.element import Element
from src.calculators.weight_calculator import calculate_weight

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
print(calculate_weight(plate))
print(calculate_weight(circle))
print(calculate_weight(tube))
print(calculate_weight(prof))


