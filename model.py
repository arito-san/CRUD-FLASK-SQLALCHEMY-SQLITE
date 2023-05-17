class Students:
    def __init__(self, cpf, name, birthdate, age, gender, grades_id):
        self.cpf = cpf
        self.name = name
        self.birthdate = birthdate
        self.age = age
        self.gender = gender
        self.grades_id = grades_id

class Grades:
    def __init__(self, id, av1, av2, average):
        self.id = id
        self.av1 = av1
        self.av2 = av2
        self.average = average