from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from .db import Base
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# engine = create_engine('postgresql+psycopg2://user:password@hostname/database_name')
engine = create_engine('postgresql://postgres:71797384@localhost/cadejo07dbhw')



try:
    Base.metadata.create_all(engine)
except SQLAlchemyError as e:
    print(f"An error occurred while creating database tables: {e}")


class Teacher(Base):
    __tablename__ = 'teachers'
    teacher_id = Column(Integer, primary_key=True)
    teacher_fullname = Column(String(120), nullable=False)


class Group(Base):
    __tablename__ = 'groups'
    group_id = Column(Integer, primary_key=True)
    group_name = Column(String(20), nullable=False)


class Student(Base):
    __tablename__ = 'students'
    student_id = Column(Integer, primary_key=True)
    student_fullname = Column(String(120), nullable=False)
    group_id = Column('group_id', ForeignKey('groups.group_id', ondelete='CASCADE'))
    group = relationship('Group', backref='students')


class Discipline(Base):
    __tablename__ = 'disciplines'
    discipline_id = Column(Integer, primary_key=True)
    discipline_name = Column(String(120), nullable=False)
    teacher_id = Column('teacher_id', ForeignKey('teachers.teacher_id', ondelete='CASCADE'))
    teacher = relationship('Teacher', backref='disciplines')


class Grade(Base):
    __tablename__ = 'grades'
    grade_id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    date_of = Column('date_of', Date, nullable=True)
    student_id = Column('student_id', ForeignKey('students.student_id', ondelete='CASCADE'))
    discipline_id = Column('discipline_id', ForeignKey('disciplines.discipline_id', ondelete='CASCADE'))
    student = relationship('Student', backref='grade')
    discipline = relationship('Discipline', backref='grade')