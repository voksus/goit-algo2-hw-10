# -*- coding: utf-8 -*-

RST = '\033[0m'
BLD = '\033[1m'
ITL = '\033[3m'
INV = '\033[7m'
RED = '\033[31'
GRN = '\033[32m'
YEL = '\033[33m'
BLU = '\033[34m'
TTL = '\033[48;2;7;95;63m'
RSC = '\033[39m'

# Визначення класу Teacher
class Teacher:
    def __init__(self, first_name: str, last_name: str, age: int, email: str, can_teach_subjects: set[str]) -> None:
        self.first_name: str = first_name
        self.last_name: str  = last_name
        self.age: int        = age
        self.email: str      = email
        self.can_teach_subjects: set[str] = set(can_teach_subjects)
        self.assigned_subjects: set[str]  = set()

def create_schedule(subjects: set[str], teachers: list[Teacher]) -> list[Teacher] | None:
    available_teachers: list[Teacher] = teachers[:]   # Робимо копію, щоб не змінювати оригінальний список викладачів
    remaining_subjects: set[str]      = set(subjects) # ...також і тут
    schedule: list[Teacher] = []

    # Поки є предмети, які ніхто не викладає
    while remaining_subjects:
        # Вибір найкращого кандидата серед тих, кого ще не додали до розкладу
        candidates: list[tuple[Teacher, set[str]]] = []

        for teacher in available_teachers:
            # Перетин предметів викладача і тих, що залишились
            coverage: set[str] = teacher.can_teach_subjects.intersection(remaining_subjects)
            
            if coverage:
                candidates.append((teacher, coverage))

        if not candidates:
            # Якщо кандидатів немає, а предмети залишились - покриття неможливе
            return None

        # Сортуємо кандидатів згідно з умовами (Жадібний підхід):
        # 1. За кількістю предметів, що покриваються (descending -> -len)
        # 2. За віком (ascending -> teacher.age)
        candidates.sort(key=lambda x: (-len(x[1]), x[0].age)) # x: tuple[Teacher, set[str]]

        # Найкращий кандидат - перший у відсортованому списку
        best_teacher: Teacher
        best_coverage: set[str]
        best_teacher, best_coverage = candidates[0]

        # Призначаємо предмети обраному викладачу
        best_teacher.assigned_subjects = best_coverage
        schedule.append(best_teacher)

        # Прибираємо покриті предмети зі списку необхідних
        remaining_subjects -= best_coverage
        
        # Видаляємо цього викладача зі списку доступних, щоб не обрати його двічі
        available_teachers.remove(best_teacher)

    return schedule


if __name__ == '__main__':
    print('\033c', end='')

    # Множина предметів, яку можливо покрити наявними викладачами
    subjects: set[str] = {'Математика', 'Фізика', 'Хімія', 'Інформатика', 'Біологія'}

    # Альтернативний набір для перевірки випадку, коли покриття неможливе
    # subjects: set[str] = {'Математика', 'Фізика', 'Хімія', 'Інформатика', 'Біологія', 'Історія'}
    
    # Список викладачів
    teachers: list[Teacher] = [
        Teacher('Олександр', 'Іваненко',   45, 'o.ivanenko@example.com',   {'Математика', 'Фізика'}     ),
        Teacher('Марія',     'Петренко',   38, 'm.petrenko@example.com',   {'Хімія'}                    ),
        Teacher('Сергій',    'Коваленко',  50, 's.kovalenko@example.com',  {'Інформатика', 'Математика'}),
        Teacher('Наталія',   'Шевченко',   29, 'n.shevchenko@example.com', {'Біологія', 'Хімія'}        ),
        Teacher('Дмитро',    'Бондаренко', 35, 'd.bondarenko@example.com', {'Фізика', 'Інформатика'}    ),
        Teacher('Олена',     'Гриценко',   42, 'o.grytsenko@example.com',  {'Біологія'}                 )
    ]

    # Виклик функції створення розкладу
    schedule: list[Teacher] | None = create_schedule(subjects, teachers)

    # Виведення розкладу
    if schedule:
        print(f'{BLD+TTL} * Розклад занять * {RST}\n')
        for teacher in schedule:
            print(f'·> {YEL}{teacher.first_name} {teacher.last_name}{RST}: {teacher.age} років, email: {BLU}{teacher.email}{RST}')
            print(f'       Викладає: {ITL+GRN}{(RSC+', '+GRN).join(teacher.assigned_subjects)}{RST}\n')
    else:
        print('Неможливо покрити всі предмети наявними викладачами.')