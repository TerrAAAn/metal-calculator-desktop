from src.domain.material import Material
from src.domain.element import Element

materials = Material.load_from_json()

steel = materials["Ст3"]

material = Element(
    params={'length' : 2000, 'width' : 1000},
    quantity=2,
    material=steel,
    element_type='лист'
)

print(material)
