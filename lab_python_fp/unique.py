# Итератор для удаления дубликатов
from gen_random import gen_random

class Unique(object):
    def __init__(self, items, **kwargs):
        ignore_case = kwargs.get("ignore_case", False)
        self.current = 0
        if ignore_case:
            temp = set()
            self._items = []
            for i in items:
                if isinstance(i,str):
                    if i.lower() not in temp:
                        temp.add(i.lower())
                        self._items.append(i)  
                else:
                    if i not in temp:
                        temp.add(i)
                        self._items.append(i)  
   
        else:
            self._items = list({i for i in items})
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= len(self._items):
            raise StopIteration
        item = self._items[self.current]
        self.current+=1
        return item
    
if __name__ == "__main__":
    data = [i for i in "waterfallF"] * 5
    for i in Unique(gen_random(100,1,5)):
        print(i, end=" ")
    print("\n____________")
    for i in Unique(data):
        print(i, end=" ")
    print("\n____________")
    for i in Unique(data, ignore_case = True):
        print(i,end=" ")
    print("\n____________")
