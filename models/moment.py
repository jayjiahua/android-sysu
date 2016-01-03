# -*- coding: utf-8 -*-
# !/usr/bin/env python

from sqlalchemy import Column, String, Integer, VARCHAR,ForeignKey, Float, Text, DateTime
from sqlalchemy.orm import relationship,backref
from utils.db import engine, Base
from datetime import datetime

class Moment(Base):
    __tablename__ = 'moment'
    id = Column(Integer, primary_key=True)
    student_id = Column(VARCHAR(20), ForeignKey('student.student_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    content = Column(Text, nullable=False)
    create_time = Column(DateTime, nullable=False)

    student = relationship('Student', backref=backref('moments', lazy='dynamic'))

    def __init__(self, student_id, content):
        self.student_id = student_id
        self.content = content
        self.create_time = datetime.now()

    def __repr__(self):
        return '<Moment - %r, %r>' % (self.student_id, self.content)

    def to_dict(self):
        return {
            "momentID": self.id,
            "student": self.student.to_dict(),
            "content": self.content,
            "time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "likeCount": self.likers.count(),
            "unlikeCount": self.unlikers.count()
        }

class MomentLike(Base):
    __tablename__ = 'moment_like'
    student_id = Column(VARCHAR(20), ForeignKey('student.student_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, primary_key=True)
    moment_id = Column(Integer, ForeignKey('moment.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, primary_key=True)
    create_time = Column(DateTime, nullable=False)

    student = relationship('Student', backref=backref('like_moments', lazy='dynamic'))
    moment = relationship('Moment', backref=backref('likers', lazy='dynamic'))

    def __init__(self, student_id, moment_id):
        self.student_id = int(student_id)
        self.moment_id = int(moment_id)
        self.create_time = datetime.now()

    def __repr__(self):
        return '<MomentLike - %r, %r>' % (self.student_id, self.moment_id)

class MomentUnlike(Base):
    __tablename__ = 'moment_unlike'
    student_id = Column(VARCHAR(20), ForeignKey('student.student_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, primary_key=True)
    moment_id = Column(Integer, ForeignKey('moment.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, primary_key=True)
    create_time = Column(DateTime, nullable=False)

    student = relationship('Student', backref=backref('unlike_moments', lazy='dynamic'))
    moment = relationship('Moment', backref=backref('unlikers', lazy='dynamic'))

    def __init__(self, student_id, moment_id):
        self.student_id = int(student_id)
        self.moment_id = int(moment_id)
        self.create_time = datetime.now()

    def __repr__(self):
        return '<MomentUnlike - %r, %r>' % (self.student_id, self.moment_id)


