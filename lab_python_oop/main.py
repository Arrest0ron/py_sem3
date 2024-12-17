from Square import Square
from Circle import Circle
from Rectangle import Rectangle
import pyfiglet 

print(pyfiglet.figlet_format("laba!", font="slant"))


def main():
    Rectangle(13,13, "синий").repr()
    Circle(13, "зеленый").repr()
    Square(13, "красный").repr()
    


if __name__ == "__main__":
    main()