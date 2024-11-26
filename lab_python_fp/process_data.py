import json
import sys
from print_result import print_result
from cm_tymer import cm_timer_1
from time import sleep
from unique import Unique
from gen_random import gen_random
# Сделаем другие необходимые импорты

path = "lab2/data/data_light.json"

# Необходимо в переменную path сохранить путь к файлу, который был передан при запуске сценария

with open(path) as f:
    data = json.load(f)
    

# Далее необходимо реализовать все функции по заданию, заменив `raise NotImplemented`
# Предполагается, что функции f1, f2, f3 будут реализованы в одну строку
# В реализации функции f4 может быть до 3 строк

@print_result
def f1(arg):
    return [i for i in Unique(list(j["job-name"] for j in arg),ignore_case = True)]


@print_result
def f2(arg):
    return [i for i in filter(lambda x: x.lstrip()[:11].lower() == "программист", arg)]


@print_result
def f3(arg):
    return list(map(lambda x: x + " с опытом Python", arg))


@print_result
def f4(arg):
    pairs = zip(arg,gen_random(len(arg),100000,200000))
    return list(i+" " + str(j) for i,j in pairs)
        

if __name__ == '__main__':
    with cm_timer_1():
        f4(f3(f2(f1(data))))