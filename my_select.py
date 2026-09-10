from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Subject, Grade

# Рядок підключення до вашої БД
URL = "postgresql://postgres:hw06pass@localhost:5432/postgres"

engine = create_engine(URL)
Session = sessionmaker(bind=engine)
session = Session()


def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    return (
        session.query(
            Student.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )


def select_2(subject_id: int):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    return (
        session.query(
            Student.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .first()
    )


def select_3(subject_id: int):
    """Знайти середній бал у групах з певного предмета."""
    return (
        session.query(
            Group.name, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .select_from(Group)
        .join(Student)
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .all()
    )


def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    # scalar() повертає єдине значення, а не список
    return session.query(func.round(func.avg(Grade.grade), 2)).scalar()


def select_5(teacher_id: int):
    """Знайти які курси читає певний викладач."""
    return session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()


def select_6(group_id: int):
    """Знайти список студентів у певній групі."""
    return session.query(Student.fullname).filter(Student.group_id == group_id).all()


def select_7(group_id: int, subject_id: int):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    return (
        session.query(Student.fullname, Grade.grade)
        .join(Group)
        .join(Grade)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .all()
    )


def select_8(teacher_id: int):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    return (
        session.query(func.round(func.avg(Grade.grade), 2))
        .select_from(Grade)
        .join(Subject)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )


def select_9(student_id: int):
    """Знайти список курсів, які відвідує певний студент."""
    return (
        session.query(Subject.name)
        .select_from(Grade)
        .join(Subject)
        .filter(Grade.student_id == student_id)
        .group_by(Subject.id)
        .all()
    )


def select_10(student_id: int, teacher_id: int):
    """Список курсів, які певному студенту читає певний викладач."""
    return (
        session.query(Subject.name)
        .select_from(Grade)
        .join(Subject)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .group_by(Subject.id)
        .all()
    )


# Блок для тестування функцій у терміналі
if __name__ == "__main__":
    print("1. Топ 5 студентів:", select_1())
    print("2. Кращий студент з предмета 1:", select_2(1))
    print("3. Середній бал груп з предмета 1:", select_3(1))
    print("4. Середній бал на потоці:", select_4())
    print("5. Курси викладача 1:", select_5(1))
    print("6. Студенти групи 1:", select_6(1))
    print("7. Оцінки групи 1 з предмета 1:", select_7(1, 1))
    print("8. Середній бал, який ставить викладач 1:", select_8(1))
    print("9. Курси студента 1:", select_9(1))
    print("10. Курси студента 1 від викладача 1:", select_10(1, 1))
