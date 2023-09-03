import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Group

parser = argparse.ArgumentParser(description='CRUD operations for groups')
parser.add_argument('--action', '-a', choices=['create', 'list', 'update', 'remove'], required=True, help='CRUD action')
parser.add_argument('--id', type=int, help='Group ID')
parser.add_argument('--name', help='Group name')

args = parser.parse_args()

db_url = 'postgresql://postgres:71797384@localhost/cadejo07dbhw'
engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

if args.action == 'create':
    if args.name:
        new_group = Group(group_name=args.name)
        session.add(new_group)
        session.commit()
        print(f'Group "{args.name}" has been created.')

elif args.action == 'list':
    groups = session.query(Group).all()
    print('List of Groups:')
    for group in groups:
        print(f'ID: {group.group_id}, Name: {group.group_name}')

elif args.action == 'update':
    if args.id and args.name:
        group = session.query(Group).filter_by(group_id=args.id).first()
        if group:
            group.group_name = args.name
            session.commit()
            print(f'Group with ID {args.id} has been updated with the name "{args.name}".')

elif args.action == 'remove':
    if args.id:
        group = session.query(Group).filter_by(group_id=args.id).first()
        if group:
            session.delete(group)
            session.commit()
            print(f'Group with ID {args.id} has been removed.')

session.close()