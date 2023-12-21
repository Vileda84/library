import os
from sqlalchemy import Boolean, create_engine, Column, Integer, String, ForeignKey, Text, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


database_path='sqlite:///library.db'
# Create an SQLite database
engine = create_engine(database_path, echo=True)

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    isbn = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=False)
    summary = Column(Text, nullable=False)
    review = Column(Integer, nullable=False)
    availability = relationship('Availability', back_populates='books')
    history=relationship('History', back_populates='books')



class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(Text)
    last_name = Column(Text)
    books = relationship('Book', back_populates='authors')


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, autoincrement=True)
    genre = Column(String)
    books = relationship('Book', back_populates='genres')


class Availability(Base):
    __tablename__ = 'availability'

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    available=Column(Boolean,nullable=False)


class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)

