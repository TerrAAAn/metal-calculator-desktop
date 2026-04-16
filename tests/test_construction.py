from src.domain.material import Material
from src.domain.element import Element
from src.domain.construction import Construction 

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
    params={'size' : "57x3,5"},
    quantity=4,
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

area_calc = AreaCalculator()
weight_calc = WeightCalculator()

gas_pipeline = Construction(
    name = 'Газопровод низкого давления',
    quantity = 1,
    elements = [tube, elbow, reducer],
    area_calculator = area_calc,
    weight_calculator = weight_calc
)

pylon = Construction(
    name = 'Опора тип 1',
    quantity= 10,
    elements=[plate, angle, prof, beam, channel],
    area_calculator = area_calc,
    weight_calculator = weight_calc
)

print(gas_pipeline)
print(pylon)