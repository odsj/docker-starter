# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import relationship

from diary.model import Base


class Journal(Base):
    __tablename__ = 'journal'

    id = Column(Integer, primary_key=True)
    writer = Column(String(50), unique=False)
    title = Column(String(50), unique=False)
    context = Column(String(2000), unique=False)
    tags = Column(String(50), unique=False)
    date = Column(Date, unique=False)
    is_public = Column(Boolean, default=False)


    def __init__(self, writer, title, context, tags, date,is_public):
        self.writer = writer
        self.title = title
        self.context = context
        self.tags = tags
        self.date = date
        self.is_public = is_public
        
    def serialize(self):
        return {
            'id': self.id,
            'writer': self.writer,
            'title': self.title,
            'context' : self.context,
            'tags' : self.tags,
            'date' : self.date,
            'is_public' : self.is_public
            # other fields that you need in the json 
        }


    def __repr__(self):
        return '<Journal %r %r>' % (self.writer, self.title)