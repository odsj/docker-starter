# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from dockerStarter.model import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    gender = Column(String(50), unique=False)
    age = Column(Integer, unique=False)


    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def __repr__(self):
        return '<Diary %r %r %r>' % (self.name, self.gender, self.age)
    
