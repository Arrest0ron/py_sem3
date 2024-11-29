from Rectangle import Rectangle

class Square(Rectangle):
    name = "Квадрат"
    def __init__(self, side : float, color : str):
        super().__init__(side, side, color)
    def area(self) -> float:
        return self._width * self._height
    def get_name(cls) -> str:
        return cls.name
    def repr(self):
        print(f"{self.get_name()} со стороной {self._width}, площадью {self.area()}, {self._color.color} цвет")