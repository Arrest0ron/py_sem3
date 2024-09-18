import math
from typing import List
import sys

class Quadratic:
    
    def __init__(self, *args, **kwargs) -> List[float]:
        self.coef = []   
        if (len(args) == 4):
            self.coef = args[1:4]
        else:
            for i in ["A","B","C"]:
                while (True):
                    try:
                        self.coef.append(float(input(f"Введите коэфициент {i}: ")))
                        break
                    except ValueError: print("Неверный коэфициент. Попробуйте снова.\n")

    def get(self):
        return self.coef[0],self.coef[1],self.coef[2]

    def solve(self) -> List:
        
        a, b,c = map(float,self.get())
        D = math.pow(b,2) - 4 * a * c
        
        if (D < 0):
            solutions = ()
        if (D == 0):
            solutions = -b / (2*a)
        if (D > 0):
            sq = math.sqrt(D)
            solutions = (-b + sq) / (2*a), (-b - sq) / (2*a)
        
        return solutions




def main(*args, **kwargs):
        
    initial = Quadratic(sys.argv).solve()
    solutions = []
    for i in initial:
        solutions.extend(Quadratic("",1,0,-i).solve())
    print(*solutions)
    return 0

if (__name__ == "__main__"): main()
    


