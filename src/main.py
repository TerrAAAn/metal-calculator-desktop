import tkinter as tk
from src.utils.data_loaders import DataLoader
from src.gui.main_window import Main_window
# for tests!!!!!!
from src.domain.base_element import Base_Element
from src.domain.calculated_element import Calculated_element
from src.domain.calculated_elements import Pipe, Sheet, Round_bar, Strip, Angle, Profile_pipe, Cap
from src.domain.reference_element import Reference_element
from src.domain.reference_elements import Beam, Channel, Elbow, Reducer
from src.domain.factory import create_element, restore_element
from src.domain.construction import Construction
from src.domain.project import Project

loader = DataLoader()

des = loader.get('steel_grades.json')
mat = des['Ст3']

def main():

    # Elements test:
    elements_list = [
        Pipe(density=mat, params={'diameter': 219, 'thickness': 6, 'length' : 12.5}, quantity=2),
        Sheet(density=mat, params={'length' : 2500, 'width' : 1250, 'thickness' : 8}, quantity=2),
        Round_bar(density=mat, params={'diameter': 50, 'length' : 3}, quantity=10),
        Strip(density=mat, params={'length' : 6, 'width' : 100, 'thickness' : 10}, quantity=5),
        Profile_pipe(density=mat, params={'length' : 6, 'width' : 80, 'height' : 40, 'thickness' : 3}, quantity=4),
        Angle(density=mat, params={'width_a' : 50, 'width_b' : 50, 'thickness' : 5, 'length' : 2}, quantity=3),
        Cap(density=mat, params={'diameter': 500, 'thickness': 16}, quantity=2)
    ]

    for el in elements_list:
        print(f'Weight: {el.get_weight()}, Area: {el.get_painting_area()};\n {el.get_display_string()}')
      
    beam = Beam(params={'size' : '10б1', 'length' : 10}, quantity=2)
    print(beam.get_weight(), beam.get_painting_area())

    channel = Channel(params={'size' : '16у', 'length' : 10}, quantity=2)
    print(channel.get_weight(), channel.get_painting_area())

    elbow = Elbow(params={'size' : '57x3,5'}, quantity=2)
    print(elbow.get_weight(), elbow.get_painting_area())

    reducer = Reducer(params={'size' : '57x32'}, quantity=2)
    print(reducer.get_weight(), reducer.get_painting_area())

    project_1 = Project('Amogus')

    construction_1 = Construction('Опора 1', 2)
    construction_1.add_element(beam)
    construction_1.add_element(Pipe(density=mat, params={'diameter': 219, 'thickness': 6, 'length' : 12.5}, quantity=2))
    
    project_1.add_construction(construction_1)
    # test_end
    root = tk.Tk()
    app = Main_window(root)
    app.project = project_1
    app.refresh_constructions_listbox()
    root.mainloop()

if __name__ == "__main__":
    main()
