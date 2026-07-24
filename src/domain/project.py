from src.domain.construction import Construction

class Project:
    def __init__(self, project_name : str = 'Новый проект'):
        self.construction_list = []
        self.project_name = project_name
    
    def add_construction(self, construction_obj):
        self.construction_list.append(construction_obj)
    
    def remove_construction(self, construction_index):
        if construction_index >= 0 and construction_index < len(self.construction_list):
            self.construction_list.pop(construction_index)
        else:
            raise IndexError('Индекс вне диапазона')
    
    def replace_construction(self, construction_index, new_construction):
        if construction_index >= 0 and construction_index < len(self.construction_list):
            self.construction_list[construction_index] = new_construction
        else:
            raise IndexError('Индекс вне диапазона')
        
    def get_construction(self, construction_index):
        if construction_index >= 0 and construction_index < len(self.construction_list):
            return(self.construction_list[construction_index]) 
        else:
            raise IndexError('Индекс вне диапазона')
        
    def get_display_string(self):
        return f'Проект: {self.project_name} Количество конструкций: {len(self.construction_list)}'
    
    def to_dict(self):
        return {
            'project_name' : self.project_name,
            'construction_list' : [c.to_dict() for c in self.construction_list]
        }
    
    @classmethod
    def from_dict(cls, data : dict):
        project = cls(data['project_name'])
        for construction_data in data['construction_list']:
            project.add_construction(Construction.from_dict(construction_data))
        return project
