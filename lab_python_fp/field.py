# Пример:
goods = [
   {'title': 'Ковер', 'price': 2000},
   {'title': 'Диван для отдыха', 'price': 5300, 'color': 'black'}
]
# field(goods, 'title') должен выдавать 'Ковер', 'Диван для отдыха'
# field(goods, 'title', 'price') должен выдавать {'title': 'Ковер', 'price': 2000}, {'title': 'Диван для отдыха', 'price': 5300}

def field(items, *args):
    assert len(args) > 0
    for i in items:
        if (len(args)>1):
            field_dict = {}
            for j in args:         
                res  = i.get(j)
                if (res is not None):
                    field_dict[j] = res
            if field_dict:
                yield field_dict
        else:
            res = i.get(args[0])
            if res:
                yield res 
            
if __name__ == "__main__":
    for i in field(goods,"title","price"):
        print(i)
        