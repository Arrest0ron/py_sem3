from operator import itemgetter

class Факультет:
    """Факультет"""
    def __init__(self, id, название, зарплата_преподавателя, университет_id):
        self.id = id
        self.название = название
        self.зарплата_преподавателя = зарплата_преподавателя
        self.университет_id = университет_id

class Университет:
    """Университет"""
    def __init__(self, id, название):
        self.id = id
        self.название = название

class ФакультетыУниверситета:
    """Связь многие-ко-многим"""
    def __init__(self, университет_id, факультет_id):
        self.университет_id = университет_id
        self.факультет_id = факультет_id

def one_to_many(университеты, факультеты):
    return [(f.название, f.зарплата_преподавателя, u.название) 
            for u in университеты 
            for f in факультеты 
            if f.университет_id == u.id]

def many_to_many(университеты, факультеты, факультеты_университетов):
    temp = [(u.название, fu.университет_id, fu.факультет_id) 
            for u in университеты 
            for fu in факультеты_университетов 
            if u.id == fu.университет_id]
    return [(f.название, f.зарплата_преподавателя, университет_название) 
            for университет_название, университет_id, факультет_id in temp
            for f in факультеты if f.id == факультет_id]

def задание_Г1(data):
    return [item for item in data if item[2].startswith('А')]

def задание_Г2(университеты, one_to_many_data):
    result = []
    for u in университеты:
        факультеты = list(filter(lambda i: i[2] == u.название, one_to_many_data))
        if факультеты:
            зарплаты = [зарплата for _, зарплата, _ in факультеты]
            max_зарплата = max(зарплаты)
            result.append((u.название, max_зарплата))
    return sorted(result, key=itemgetter(1), reverse=True)

def задание_Г3(университеты, many_to_many_data):
    result = {}
    for u in университеты:
        факультеты = list(filter(lambda i: i[2] == u.название, many_to_many_data))
        факультеты_названия = [название for название, _, _ in факультеты]
        result[u.название] = факультеты_названия
    return result
