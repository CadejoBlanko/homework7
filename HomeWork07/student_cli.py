import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Student 

parser = argparse.ArgumentParser(description='CRUD operations for students')
parser.add_argument('--action', '-a', choices=['create', 'list', 'update', 'remove'], required=True, help='CRUD action')
parser.add_argument('--id', type=int, help='Student ID')
parser.add_argument('--name', help='Student name')
parser.add_argument('--group_id', type=int, help='Group ID')

args = parser.parse_args()

db_url = 'postgresql://postgres:71797384@localhost/cadejo07dbhw'
engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

if args.action == 'create':
    if args.name and args.group_id:
        new_student = Student(student_fullname=args.name, group_id=args.group_id)
        session.add(new_student)
        session.commit()
        print(f'Student "{args.name}" has been created.')

elif args.action == 'list':
    students = session.query(Student).all()
    print('List of Students:')
    for student in students:
        print(f'ID: {student.student_id}, Name: {student.student_fullname}, Group ID: {student.group_id}')

elif args.action == 'update':
    if args.id and args.name:
        student = session.query(Student).filter_by(student_id=args.id).first()
        if student:
            student.student_fullname = args.name
            session.commit()
            print(f'Student with ID {args.id} has been updated with the name "{args.name}".')

elif args.action == 'remove':
    if args.id:
        student = session.query(Student).filter_by(student_id=args.id).first()
        if student:
            session.delete(student)
            session.commit()
            print(f'Student with ID {args.id} has been removed.')

session.close()