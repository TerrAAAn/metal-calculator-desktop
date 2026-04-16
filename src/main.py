import tkinter as tk
from src.gui.main_window import MainWindow
from src.utils.data_loaders import DataLoader
from src.calculators.weight_calculator import WeightCalculator
from src.calculators.area_calculator import AreaCalculator
# for tests!!!!!!
from src.domain.construction import Construction



def main():
    root = tk.Tk()

    data_loader = DataLoader()
    weight_calc = WeightCalculator()
    ara_calc = AreaCalculator()

    # for tests!!!!!!
    test_cons1 = Construction(name="Опора 1", quantity=2, elements=[], weight_calculator= weight_calc,area_calculator= ara_calc)
    test_cons2 = Construction(name="Газопровод", quantity=1, elements=[], weight_calculator= weight_calc,area_calculator= ara_calc)
    
    app = MainWindow(root, weight_calc, ara_calc, data_loader)
    # for tests!!!!!!
    app.constructions.append(test_cons1)
    app.constructions.append(test_cons2)

    app.refresh_list()
    root.mainloop()

if __name__ == "__main__":
    main()
