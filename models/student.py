# -*- coding: utf-8 -*-
# !/usr/bin/env python

from sqlalchemy import Column, String, Integer, VARCHAR,ForeignKey, Float
from sqlalchemy.orm import relationship,backref
from utils.db import engine, Base

class Student(Base):
    __tablename__ = 'student'
    student_id = Column(VARCHAR(20), primary_key = True)
    name = Column(VARCHAR(40))
    sex = Column(VARCHAR(20))
    class_name = Column(VARCHAR(100))
    school = Column(VARCHAR(100))
    major = Column(VARCHAR(100))
    grade = Column(VARCHAR(100))

    def __init__(self, student_id, name, sex, class_name, school, major, grade):
        self.student_id = student_id
        self.name = name
        self.sex = sex
        self.class_name = class_name
        self.school = school
        self.major = major
        self.grade = grade

    def __repr__(self):
        return '<Student - %r>' % (self.student_id)

    def to_dict(self):
        return {
            "studentID": self.student_id,
            "name": self.name,
            "sex": self.sex,
            "className": self.class_name,
            "school": self.school,
            "major": self.major,
            "grade": self.grade
        }

