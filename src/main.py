import tkinter as tk
from src.utils.data_loaders import DataLoader
# for tests!!!!!!
from src.domain.base_element import Base_Element
from src.domain.calculated_element import Calculated_element
from src.domain.pipe import Pipe

loader = DataLoader()

des = loader.get('steel_grades.json')
mat = des['Ст3']
def main():
    pipe = Pipe(length=12.5, density=mat, params={"diameter": 219, "wall_thickness": 6}, quantity=2)
    print(pipe.get_weight())
    print(pipe.get_surface_area())

if __name__ == "__main__":
    main()
