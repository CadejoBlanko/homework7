import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Discipline 

parser = argparse.ArgumentParser(description='CRUD operations for disciplines')
parser.add_argument('--action', '-a', choices=['create', 'list', 'update', 'remove'], required=True, help='CRUD action')
parser.add_argument('--id', type=int, help='Discipline ID')
parser.add_argument('--name', help='Discipline name')
parser.add_argument('--teacher_id', type=int, help='Teacher ID')

args = parser.parse_args()

db_url = 'postgresql://postgres:71797384@localhost/cadejo07dbhw'
engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

if args.action == 'create':
    if args.name and args.teacher_id:
        new_discipline = Discipline(discipline_name=args.name, teacher_id=args.teacher_id)
        session.add(new_discipline)
        session.commit()
        print(f'Discipline "{args.name}" has been created.')

elif args.action == 'list':
    disciplines = session.query(Discipline).all()
    print('List of Disciplines:')
    for discipline in disciplines:
        print(f'ID: {discipline.discipline_id}, Name: {discipline.discipline_name}, Teacher ID: {discipline.teacher_id}')

elif args.action == 'update':
    if args.id and args.name:
        discipline = session.query(Discipline).filter_by(discipline_id=args.id).first()
        if discipline:
            discipline.discipline_name = args.name
            session.commit()
            print(f'Discipline with ID {args.id} has been updated with the name "{args.name}".')

elif args.action == 'remove':
    if args.id:
        discipline = session.query(Discipline).filter_by(discipline_id=args.id).first()
        if discipline:
            session.delete(discipline)
            session.commit()
            print(f'Discipline with ID {args.id} has been removed.')

session.close()