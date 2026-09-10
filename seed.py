import random
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Імпортуємо ваші моделі
from models import Group, Teacher, Student, Subject, Grade

# Рядок підключення до вашого Docker-контейнера
URL = "postgresql://postgres:hw06pass@localhost:5432/postgres"

# Ініціалізація підключення та сесії
engine = create_engine(URL)
Session = sessionmaker(bind=engine)
session = Session()

# Ініціалізація Faker (з українською локалізацією)
fake = Faker("uk_UA")


def seed_data():
    # 1. Створення 3 груп
    groups = [Group(name=f"Група {fake.word().capitalize()}-{i}") for i in range(1, 4)]
    session.add_all(groups)
    session.commit()  # Зберігаємо, щоб отримати їхні ID

    # 2. Створення 5 викладачів
    teachers = [Teacher(fullname=fake.name()) for _ in range(5)]
    session.add_all(teachers)
    session.commit()

    # 3. Створення 8 предметів із прив'язкою до випадкових викладачів
    subject_names = [
        "Математика",
        "Фізика",
        "Історія",
        "Програмування",
        "Бази даних",
        "Англійська",
        "Філософія",
        "Алгоритми",
    ]
    subjects = [
        Subject(name=name, teacher_id=random.choice(teachers).id)
        for name in subject_names
    ]
    session.add_all(subjects)
    session.commit()

    # 4. Створення 50 студентів із прив'язкою до випадкових груп
    students = [
        Student(fullname=fake.name(), group_id=random.choice(groups).id)
        for _ in range(50)
    ]
    session.add_all(students)
    session.commit()

    # 5. Створення до 20 оцінок для кожного студента
    grades = []
    for student in students:
        # Кожному студенту генеруємо від 15 до 20 оцінок
        for _ in range(random.randint(15, 20)):
            # Випадкова дата в межах останнього року (навчального процесу)
            random_date = datetime.now() - timedelta(days=random.randint(0, 365))

            grade = Grade(
                grade=random.randint(1, 100),  # Оцінка за 100-бальною шкалою
                grade_date=random_date.date(),
                student_id=student.id,
                subject_id=random.choice(subjects).id,
            )
            grades.append(grade)

    session.add_all(grades)
    session.commit()
    print("Базу даних успішно заповнено!")


if __name__ == "__main__":
    seed_data()
