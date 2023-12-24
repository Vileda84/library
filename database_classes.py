import os
from sqlalchemy import Boolean, create_engine, Column, Integer, String, ForeignKey, Text, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


database_path='sqlite:///library.db'

engine = create_engine(database_path, echo=True)

# Parent class
Base = declarative_base()

# Child class Book table
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    isbn = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=False)
    review = Column(Integer, nullable=False)
    author=relationship('Author', backref='books')
    genre=relationship('Genre', backref='books')


# Child class Author Table
class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(Text)
    last_name = Column(Text)

# Child class Genre table
class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, autoincrement=True)
    genre = Column(String)

# Child class Availability table
class Availability(Base):
    __tablename__ = 'availability'

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    available=Column(Boolean,nullable=False)
    books = relationship('Book', backref='availability')

# Child class History table
class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    books = relationship('Book', backref='history')