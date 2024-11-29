class Color:
    def __init__(self, color : str):
        self.color = color
    
    @property
    def color(self) -> str:
        return self._color
    
    @color.setter
    def color(self, color : str):
        self._color = color