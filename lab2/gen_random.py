from random import randint
# Пример:
# gen_random(5, 1, 3) должен выдать выдать 5 случайных чисел
# в диапазоне от 1 до 3, например 2, 2, 3, 2, 1
# Hint: типовая реализация занимает 2 строки
def gen_random(num_count, begin, end):
    
    for _ in range(num_count):
        yield randint(begin,end)
if __name__ == "__main__":       
    for i in gen_random(5,1,3):
        print(i)
