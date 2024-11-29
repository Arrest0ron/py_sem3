from Color import Color
from AbstractShape import AbstractShape

class Rectangle(AbstractShape):
    name = "Прямоугольник" 
    def __init__(self, width : float, height : float, color : str):
        self._width = width
        self._height = height
        self._color = Color(color)
        
    def area(self) -> float:
        return self._width * self._height
    def get_name(cls) -> str:
        return cls.name
    
    def repr(self):
        print(f"{self.get_name()} ширины {self._width}, высоты {self._height}, площадью {self.area()}, {self._color.color} цвет")
        
        