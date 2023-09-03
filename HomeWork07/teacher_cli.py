import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Teacher

parser = argparse.ArgumentParser(description='CRUD operations for teachers')
parser.add_argument('--action', '-a', choices=['create', 'list', 'update', 'remove'], required=True, help='CRUD action')
parser.add_argument('--model', '-m', choices=['Teacher'], required=True, help='Model name')

parser.add_argument('--id', type=int, help='Teacher ID')
parser.add_argument('--name', help='Teacher name')

args = parser.parse_args()

db_url = 'postgresql://postgres:password@localhost/mydb'
engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

if args.action == 'create':
    if args.model == 'Teacher':
        new_teacher = Teacher(name=args.name)
        session.add(new_teacher)
        session.commit()
        print(f'Teacher "{args.name}" has been created.')

elif args.action == 'list':
    if args.model == 'Teacher':
        teachers = session.query(Teacher).all()
        print('List of Teachers:')
        for teacher in teachers:
            print(f'ID: {teacher.id}, Name: {teacher.name}')

elif args.action == 'update':
    if args.model == 'Teacher' and args.id is not None and args.name is not None:
        teacher = session.query(Teacher).filter_by(id=args.id).first()
        if teacher:
            teacher.name = args.name
            session.commit()
            print(f'Teacher with ID {args.id} has been updated with the name "{args.name}".')

elif args.action == 'remove':
    if args.model == 'Teacher' and args.id is not None:
        teacher = session.query(Teacher).filter_by(id=args.id).first()
        if teacher:
            session.delete(teacher)
            session.commit()
            print(f'Teacher with ID {args.id} has been removed.')

session.close()