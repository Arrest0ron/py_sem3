import math
from typing import List
import sys

def SolveQuadratic(Equation: List) -> List:
    
    a, b,c = map(float,Equation)
    D = math.pow(b,2) - 4 * a * c

    if (D < 0):
        solutions = ()
    if (D == 0):
        solutions = -b / (2*a)
    if (D > 0):
        sq = math.sqrt(D)
        solutions = (-b + sq) / (2*a), (-b - sq) / (2*a)
    return solutions



def initialization():
    coef = []   
    arg = sys.argv
    if (len(arg) > 1):
        coef = arg[1:4]
    else:
        for i in ["A","B","C"]:
            while (True):
                try:
                    coef.append(float(input(f"Введите коэфициент {i}: ")))
                    break
                except ValueError: print("Неверный коэфициент. Попробуйте снова.\n")
                except: return -1
                
    return coef
                
def main(*args, **kwargs):

    coef = initialization()
    quadratic_solutions = SolveQuadratic(coef)
    solutions = []
    for i in quadratic_solutions:
        solutions.extend(SolveQuadratic([1,0,-i]))
    print(*solutions)
    return 0

if (__name__ == "__main__"): main()
    


