from abc import ABC, abstractmethod

class Base_Element(ABC):
    def __init__(self, quantity: int = 1):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        self.quantity = quantity

    @abstractmethod
    def get_weight(self):
        pass
    
    @abstractmethod
    def get_painting_area(self):
        pass
    
   # @abstractmethod
   # def get_display_string(self):
   #     pass

   # @abstractmethod
   # def get_params_dict(self):
   #     pass
    