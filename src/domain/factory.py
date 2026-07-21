from src.domain.calculated_element import Calculated_element
from src.domain.reference_element import Reference_element
from src.domain.calculated_elements import Pipe, Sheet, Strip, Profile_pipe, Round_bar, Cap, Angle
from src.domain.reference_elements import Beam, Channel, Elbow, Reducer

ELEMENT_CLASSES = {
    'Pipe' : Pipe,
    'Sheet' : Sheet,
    'Strip' : Strip,
    'Profile_pipe' : Profile_pipe,
    'Round_bar' : Round_bar,
    'Cap' : Cap,
    'Angle' : Angle,
    'Beam' : Beam,
    'Channel' : Channel,
    'Elbow' : Elbow,
    'Reducer' : Reducer 
}

def create_element(name: str, params: dict, density: int, quantity: int = 1):
    element_class = ELEMENT_CLASSES.get(name)
    if element_class is None:
        raise ValueError('f Элемента {name} не существует')
    elif issubclass(element_class, Calculated_element):
        return element_class(
            density = density,
            params = params,
            quantity = quantity
        )
    elif issubclass(element_class, Reference_element):
        return element_class(
            params= params,
            quantity= quantity
        )

def restore_element(params_dict : dict):
    name = params_dict.get('element_name')

    if name not in ELEMENT_CLASSES:
        raise ValueError(f"Элемента '{name}' не существует")
    
    element_class = ELEMENT_CLASSES.get(name)
    
    if 'density' in params_dict.keys():
        return element_class(
            density = params_dict['density'],
            params = params_dict['params'],
            quantity = params_dict['quantity']
        )
    else:
        return element_class(
            params = params_dict['params'],
            quantity = params_dict['quantity']
        )
    