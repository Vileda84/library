from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


# Parent class
Base = declarative_base()

# Subclass Book table
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


# Subclass Author Table
class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(Text)
    last_name = Column(Text)

# Subclass Genre table
class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, autoincrement=True)
    genre = Column(String)

# Subclass Availability table
class Availability(Base):
    __tablename__ = 'availability'

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    available=Column(Boolean,nullable=False)
    books = relationship('Book', backref='availability')

# Subclass History table
class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    books = relationship('Book', backref='history')