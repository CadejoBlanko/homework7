from datetime import date, datetime, timedelta
from random import randint, choice
import faker
from sqlalchemy import select

from src.models import Teacher, Student, Discipline, Grade, Group
from src.db import session


def date_range(start: date, end: date) -> list:
    result = []
    current_date = start
    while current_date <= end:
        if current_date.isoweekday() < 6:
            result.append(current_date)
        current_date += timedelta(1)
    return result


def fill_data():
    disciplines = [
        "Вища математика",
        "Фізика",
        "Основи програмування",
        "Об'єктно-орієнтоване програмування",
        "Історія України",
        "Веб-технології та розробка веб-додатків",
        "Нейросетельні технології та системи"
    ]

    groups = ["122_1_23", "122_2_23", "122_3_23"]

    fake = faker.Faker()
    NUMDEFR_OF_TRACHERS = 5
    NUMBER_OF_STUDENTS = 30

    def seed_teachers():
        for _ in range(NUMDEFR_OF_TRACHERS):
            teacher = Teacher(teacher_fullname=fake.name())
            session.add(teacher)
        session.commit()

    def seed_disciplines():
        teacher_ids = session.scalars(select(Teacher.teacher_id)).all()
        for discipline in disciplines:
            session.add(Discipline(discipline_name=discipline, teacher_id=choice(teacher_ids)))
        session.commit()

    def seed_groups():
        for group in groups:
            session.add(Group(group_name=group))
        session.commit()

    def seed_students():
        group_ids = session.scalars(select(Group.group_id)).all()
        for _ in range(NUMBER_OF_STUDENTS):
            student = Student(student_fullname=fake.name(), group_id=choice(group_ids))
            session.add(student)
        session.commit()

    def seed_grades():
        start_date = datetime.strptime("2023-09-01", "%Y-%m-%d")
        end_date = datetime.strptime("2024-05-25", "%Y-%m-%d")
        d_range = date_range(start=start_date, end=end_date)
        discipline_ids = session.scalars(select(Discipline.discipline_id)).all()
        student_ids = session.scalars(select(Student.student_id)).all()

        for d in d_range:  
            random_id_discipline = choice(discipline_ids)
            random_ids_student = [choice(student_ids) for _ in range(5)]
            for student_id in random_ids_student:
                grade = Grade(
                    grade=randint(1, 12),
                    date_of=d,
                    student_id=student_id,
                    discipline_id=random_id_discipline,
                )
                session.add(grade)
        session.commit()

    seed_teachers()
    seed_disciplines()
    seed_groups()
    seed_students()
    seed_grades()


if __name__ == "__main__":
    fill_data()