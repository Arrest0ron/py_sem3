from Color import Color
from AbstractShape import AbstractShape
from math import pi

class Circle(AbstractShape):
    name = "Круг"
    def __init__(self, radius : float, color : str):
        self._radius = radius
        self._color = Color(color)
        
    def area(self) -> float:
        return pi*self._radius**2
    def get_name(cls) -> str:
        return cls.name
    
    def repr(self):
        print(f"{self.get_name()} с радиусом {self._radius}, площадью {self.area():.4f}, {self._color.color} цвет")