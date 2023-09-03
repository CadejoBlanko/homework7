from sqlalchemy import func
from sqlalchemy.orm import Session
from src.models import Student, Discipline, Grade, Teacher, Group

def select_1(session: Session):

    students = session.query(Student).all()
    students_with_avg_grades = []

    for student in students:
        avg_grade = session.query(func.avg(Grade.grade)).filter(Grade.student_id == student.student_id).scalar()
        students_with_avg_grades.append((student, avg_grade))

    students_with_avg_grades.sort(key=lambda x: x[1], reverse=True)
    return students_with_avg_grades[:5]

def select_2(session: Session, discipline_name):

    discipline = session.query(Discipline).filter(Discipline.discipline_name == discipline_name).first()
    if not discipline:
        return None

    students = session.query(Student).all()
    students_with_avg_grades = []

    for student in students:
        avg_grade = session.query(func.avg(Grade.grade)).filter(
            Grade.student_id == student.student_id,
            Grade.discipline_id == discipline.discipline_id
        ).scalar()
        students_with_avg_grades.append((student, avg_grade))

    students_with_avg_grades.sort(key=lambda x: x[1], reverse=True)
    return students_with_avg_grades[0]

def select_3(session: Session, discipline_name):
    
    discipline = session.query(Discipline).filter(Discipline.discipline_name == discipline_name).first()
    if not discipline:
        return None

    groups = session.query(Group).all()
    avg_grades_in_groups = []

    for group in groups:
        students_in_group = session.query(Student).filter(Student.group_id == group.id).all()
        total_avg_grade = 0

        for student in students_in_group:
            avg_grade = session.query(func.avg(Grade.grade)).filter(
                Grade.student_id == student.student_id,
                Grade.discipline_id == discipline.discipline_id
            ).scalar()
            if avg_grade:
                total_avg_grade += avg_grade

        if students_in_group:
            group_avg_grade = total_avg_grade / len(students_in_group)
            avg_grades_in_groups.append((group, group_avg_grade))

    return avg_grades_in_groups

def select_4(session: Session):
   
    avg_grade = session.query(func.avg(Grade.grade)).scalar()
    return avg_grade

def select_5(session: Session, teacher_name):

    teacher = session.query(Teacher).filter(Teacher.teacher_fullname == teacher_name).first()
    if not teacher:
        return None

    disciplines_taught_by_teacher = session.query(Discipline).filter(Discipline.teacher_id == teacher.id).all()
    return [discipline.name for discipline in disciplines_taught_by_teacher]

def select_6(session: Session, group_name):

    group = session.query(Group).filter(Group.group_name == group_name).first()
    if not group:
        return None

    students_in_group = session.query(Student).filter(Student.group_id == group.group_id).all()
    return [student.student_fullname for student in students_in_group]

def select_7(session: Session, group_name, discipline_name):
  
    group = session.query(Group).filter(Group.group_name == group_name).first()
    if not group:
        return None

    discipline = session.query(Discipline).filter(Discipline.discipline_name == discipline_name).first()
    if not discipline:
        return None

    students_in_group = session.query(Student).filter(Student.group_id == group.group_id).all()
    grades = []

    for student in students_in_group:
        student_grades = session.query(Grade).filter(
            Grade.student_id == student.student_id,
            Grade.discipline_id == discipline.discipline_id
        ).all()
        grades.extend([(student.student_fullname, grade.grade) for grade in student_grades])

    return grades

def select_8(session: Session, teacher_name):

    teacher = session.query(Teacher).filter(Teacher.teacher_fullname == teacher_name).first()
    if not teacher:
        return None

    disciplines_taught_by_teacher = session.query(Discipline).filter(Discipline.teacher_id == teacher.teacher_id).all()
    total_avg_grade = 0
    count = 0

    for discipline in disciplines_taught_by_teacher:
        student_grades = session.query(Grade.grade).filter(Grade.discipline_id == discipline.discipline_id).all()
        if student_grades:
            avg_grade = sum([grade[0] for grade in student_grades]) / len(student_grades)
            total_avg_grade += avg_grade
            count += 1

    if count > 0:
        teacher_avg_grade = total_avg_grade / count
        return teacher_avg_grade

def select_9(session: Session, student_name):
   
    student = session.query(Student).filter(Student.student_fullname == student_name).first()
    if not student:
        return None

    student_disciplines = session.query(Discipline).join(Grade).filter(Grade.student_id == student.student_id).all()
    return [discipline.discipline_name for discipline in student_disciplines]

def select_10(session: Session, student_name, teacher_name):

    student = session.query(Student).filter(Student.student_fullname == student_name).first()
    if not student:
        return None

    teacher = session.query(Teacher).filter(Teacher.teacher_fullname == teacher_name).first()
    if not teacher:
        return None

    student_disciplines = session.query(Discipline).join(Grade).filter(
        Grade.student_id == student.student_id,
        Discipline.teacher_id == teacher.teacher_id
    ).all()
    
    return [discipline.name for discipline in student_disciplines]