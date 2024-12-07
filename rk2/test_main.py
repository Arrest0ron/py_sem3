import unittest
from main import ФакультетыУниверситета, Университет, Факультет, one_to_many, задание_Г1, задание_Г2,  задание_Г3, many_to_many
class TestФакультеты(unittest.TestCase):
    def setUp(self):
        self.университеты = [
            Университет(1, 'МГУ'),
            Университет(2, 'СПбГУ'),
            Университет(3, 'МФТИ'),
            Университет(4, 'АГУ')
        ]
        self.факультеты = [
            Факультет(1, 'Математический', 50000, 1),
            Факультет(2, 'Физический', 60000, 1),
            Факультет(3, 'Исторический', 45000, 2),
            Факультет(4, 'Биологический', 55000, 3),
            Факультет(5, 'Астрономический', 70000, 4)
        ]
        self.факультеты_университетов = [
            ФакультетыУниверситета(1, 1),
            ФакультетыУниверситета(1, 2),
            ФакультетыУниверситета(2, 3),
            ФакультетыУниверситета(3, 4),
            ФакультетыУниверситета(4, 5)
        ]
        self.one_to_many_data = one_to_many(self.университеты, self.факультеты)
        self.many_to_many_data = many_to_many(self.университеты, self.факультеты, self.факультеты_университетов)

    def test_задание_Г1(self):
        expected = [('Астрономический', 70000, 'АГУ')]
        result = задание_Г1(self.one_to_many_data)
        self.assertEqual(result, expected)

    def test_задание_Г2(self):
        expected = [('АГУ', 70000),('МГУ', 60000),  ('МФТИ', 55000), ('СПбГУ', 45000)]
        result = задание_Г2(self.университеты, self.one_to_many_data)
        self.assertEqual(result, expected)

    def test_задание_Г3(self):
        expected = {
            'МГУ': ['Математический', 'Физический'],
            'СПбГУ': ['Исторический'],
            'МФТИ': ['Биологический'],
            'АГУ': ['Астрономический']
        }
        result = задание_Г3(self.университеты, self.many_to_many_data)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()