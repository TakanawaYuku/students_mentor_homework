class MembersTraining:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        if type(self) == Student or type(self) == Lecturer:
            self.grades = {}
        if type(self) == Student:
            self.courses_in_progress = []
        if isinstance(self, Mentor):
            self.courses_attached = []

    @property
    def middle_grade(self):
        gen = (i for j in self.grades.values() for i in j)
        count, total = 0, 0
        for i in gen:
            count += 1
            total += i
        return round(total / count, 1)

    def __eq__(self, other):
        if type(self) == Reviewer:
            return 'Не поддерживается сравнение'
        elif type(self) == type(other):
            return self.middle_grade == other.middle_grade

    def __lt__(self, other):
        if type(self) == Reviewer:
            return 'Не поддерживается сравнение'
        elif type(self) == type(other):
            return self.middle_grade < other.middle_grade

    def __le__(self, other):
        return self == other or self < other

    def __rate_true(self, people, course):
        if type(self) == Student:
            return isinstance(people,
                              Lecturer) and course in self.courses_in_progress and course in people.courses_attached
        elif type(self) == Reviewer:
            return isinstance(people,
                              Student) and course in self.courses_attached and course in people.courses_in_progress
        else:
            print('Нет прав для проставления оценки')

    def rate_homework(self, people, course, grade):
        if self.__rate_true(people, course):
            if course in people.grades:
                people.grades[course] += [grade]
            else:
                people.grades[course] = [grade]


class Student(MembersTraining):
    students = []

    def __init__(self, name, surname, gender):
        super().__init__(name, surname, gender)
        self.finished_courses = []
        Student.students.append(self)

    def __str__(self):
        return f'''
Имя: {self.name}
Фамилия: {self.surname}
Средняя оценка за домашние задания: {self.middle_grade}
Курсы в процессе изучения: {', '.join(self.courses_in_progress)}
Завершенные курсы: {', '.join(self.finished_courses)}
'''

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)


class Mentor(MembersTraining):
    def __init__(self, name, surname, gender):
        super().__init__(name, surname, gender)


class Lecturer(Mentor):
    lecturers = []
    def __init__(self, name, surname, gender):
        super().__init__(name, surname, gender)
        Lecturer.lecturers.append(self)

    def __str__(self):
        return f'''
Имя: {self.name}
Фамилия: {self.surname}
Средняя оценка за лекции: {self.middle_grade}
'''


class Reviewer(Mentor):
    def __init__(self, name, surname, gender):
        super().__init__(name, surname, gender)

    def __str__(self):
        return f'''Имя: {self.name}
Фамилия: {self.surname}
'''


def grade_mid(course, peoples):
    if peoples == Student.students:
        row = 'по всем домашним заданиям cтудентов'
    else:
        row = 'по всем лекторам'

    count, total = 0, 0
    for people in peoples:
        if course in people.grades:
            for grade in people.grades[course]:
                total += grade
                count += 1
    return f'Средняя оценка {row} по курсу "{course}": {round(total / count, 1)}'


student1 = Student('Филипп', 'Киркоров', 'муж')
student2 = Student('Алла', 'Пугачева', 'жен')
lector1 = Lecturer('Надежда', 'Бабкина', 'жен')
lector2 = Lecturer('Семен', 'Слепаков', 'муж')
reviewer1 = Reviewer('Валерий', 'Меладзе', 'муж')
reviewer2 = Reviewer('Полина', 'Гагарина', 'жен')

student1.courses_in_progress += ['Python', 'С++']
student1.finished_courses += ['Введение в программирование']
student2.courses_in_progress += ['Python', 'С++', 'Git']
student2.finished_courses += ['Введение в программирование']
lector1.courses_attached += ['Python', 'С++']
lector2.courses_attached += ['Python', 'С++', 'Git']
reviewer1.courses_attached += ['Python', 'С++']
reviewer2.courses_attached += ['Python', 'С++', 'Git']

reviewer1.rate_homework(student1, 'Python', 7)
reviewer1.rate_homework(student1, 'С++', 10)
reviewer2.rate_homework(student2, 'Python', 7)
reviewer2.rate_homework(student2, 'С++', 8)
reviewer2.rate_homework(student2, 'Git', 9)

student1.rate_homework(lector1, 'Python', 5)
student1.rate_homework(lector1, 'С++', 9)
student2.rate_homework(lector1, 'Python', 10)
student2.rate_homework(lector1, 'С++', 6)

student1.rate_homework(lector2, 'Python', 5)
student1.rate_homework(lector2, 'С++', 10)
student2.rate_homework(lector2, 'Python', 7)
student2.rate_homework(lector2, 'С++', 10)
student2.rate_homework(lector2, 'Git', 8)

print(student1)
print(student2)

print(lector1)
print(lector2)
print(reviewer1)
print(reviewer2)

print(grade_mid('Python', Student.students))
print(grade_mid('С++', Student.students))
print(grade_mid('Git', Lecturer.lecturers))
print(grade_mid('С++', Lecturer.lecturers))

print(lector1 < lector2)
print(student1 == student2)
print(reviewer1 == reviewer2)
lector1.rate_homework(student2, 'Git', 10)