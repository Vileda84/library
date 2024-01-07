from faker import Faker
import random
from database_classes import *
from sqlalchemy.orm import sessionmaker



def generate_fake_book():
    """Creates fake data for books table
    returns: dictionary of book data
    """
    fake=Faker()
    fake_name=f'book{random.randint(1,100)}'
    fake_isbn=fake.isbn10()
    fake_author=random.randint(1,10)
    fake_genre=random.randint(1,5)
    fake_review=random.randint(1,5)

    return Book(
            name=fake_name,
            isbn=fake_isbn,
            author_id=fake_author,
            genre_id=fake_genre,
            review=fake_review
        )

def insert_books(num_books,engine):
    """Inserts the data on books table

    Args:
        num_books (integer):number of rows
    """
    Session = sessionmaker(bind=engine)
    session = Session()

    for _ in range(num_books):
        new_book = generate_fake_book()
        session.add(new_book)
        session.commit()

def generate_fake_availability(i):
    """Creates fake data for availabilty table
    returns: dictionary of availability data
    """
    fake_book_id=i
    fake_available=random.choice([True, False])

    return Availability(
        book_id=fake_book_id,
        available=fake_available
    )

def insert_availability(num_books,engine):
    """Inserts the data on availabilty table

    Args:
        num_books (integer):number of rows
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    for i in range(num_books):
        new_availability = generate_fake_availability(i)
        session.add(new_availability)
        session.commit()


def generate_fake_author():
    """Creates fake data for authors table
    returns: dictionary of authors data
    """
    fake=Faker()
    fake_first_name=fake.first_name()
    fake_last_name=fake.last_name()

    return Author(
        first_name=fake_first_name,
        last_name=fake_last_name
    )

def insert_authors(num_authors,engine):
    """Inserts the data on authors table

    Args:
        num_authors (integer):number of rows
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    for _ in range(num_authors):
        new_author = generate_fake_author()
        session.add(new_author)
        session.commit()


def generate_fake_genre():
    """Creates fake data for genres table
    returns: dictionary of genre data
    """
    fake_name=f'genre{random.randint(1,5)}'

    return Genre(
        genre=fake_name
    )

def insert_genres(num_genres,engine):
    """Inserts the data on books table

    Args:
        num_books (integer):number of rows
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    for _ in range(num_genres):
        new_genre = generate_fake_genre()
        session.add(new_genre)
        session.commit()

def generate_fake_user_history():
    """Creates fake data for user_history table
    returns: dictionary of user_history data
    """
    fake_book_id=random.randint(1,50)

    return History(
        book_id=fake_book_id
    )

def insert_user_history(num_books,engine):
    """Inserts the data on books table

    Args:
        num_books (integer):number of rows
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    for _ in range(num_books):
        new_history = generate_fake_user_history()
        session.add(new_history)
        session.commit()














