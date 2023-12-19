from faker import Faker
import random
from database import *



def generate_fake_book():
    """Creates fake data for books table
    returns: dictionary of book data
    """
    fake=Faker()
    fake_name=f'book{random.randint(1,100)}'
    fake_isbn=fake.isbn10()
    fake_author=random.randint(1,10)
    fake_genre=random.randint(1,5)
    fake_summary=fake.text(max_nb_chars=160)
    fake_review=random.randint(1,5)

    return{
        'name':fake_name,
        'isbn':fake_isbn,
        'author_id':fake_author,
        'genre_id':fake_genre,
        'summary':fake_summary,
        'review':fake_review
    }

def insert_books(num_books):
    """Inserts the data on books table

    Args:
        num_books (integer):number of rows
    """
    database = r"C:\sqlite\db\library.db"
    conn = create_connection(database)
    for _ in range(num_books):
        book=generate_fake_book()
        book_values=(book['name'],book['isbn'],book['author_id'],book['genre_id'], book['summary'], book['review'])
        book_id=create_new_book(conn, book_values)

def generate_fake_availability(i):
    """Creates fake data for availabilty table
    returns: dictionary of availability data
    """
    fake_book_id=i
    fake_available=random.choice([True, False])

    return{
        'book_id':fake_book_id,
        'available':fake_available
    }

def insert_availability(num_books):
    """Inserts the data on availabilty table

    Args:
        num_books (integer):number of rows
    """
    database = r"C:\sqlite\db\library.db"
    conn = create_connection(database)
    for i in range(num_books):
        availability=generate_fake_availability(i)
        availability_values=(availability['book_id'],availability['available'])
        availability_id=create_new_availability(conn, availability_values)


def generate_fake_author():
    """Creates fake data for authors table
    returns: dictionary of authors data
    """
    fake=Faker()
    fake_first_name=fake.first_name()
    fake_last_name=fake.last_name()

    return{
        'first_name':fake_first_name,
        'last_name':fake_last_name
    }

def insert_authors(num_authors):
    """Inserts the data on authors table

    Args:
        num_authors (integer):number of rows
    """
    database = r"C:\sqlite\db\library.db"
    conn = create_connection(database)
    for _ in range(num_authors):
        author=generate_fake_author()
        author_values=(author['first_name'],author['last_name'])
        author_id=create_new_author(conn, author_values)


def generate_fake_genre():
    """Creates fake data for genres table
    returns: dictionary of genre data
    """
    fake_name=f'genre{random.randint(1,5)}'

    return{
        'genre':fake_name
    }

def insert_genres(num_genres):
    """Inserts the data on books table

    Args:
        num_books (integer):number of rows
    """
    database = r"C:\sqlite\db\library.db"
    conn = create_connection(database)
    for _ in range(num_genres):
        genre=generate_fake_genre()
        genre_values=[genre['genre']]
        genre_id=create_new_genre(conn, genre_values)

def generate_fake_user_history():
    """Creates fake data for user_history table
    returns: dictionary of user_history data
    """
    fake_book_id=random.randint(1,50)

    return{
        'book_id':fake_book_id
    }

def insert_user_history(num_books):
    """Inserts the data on books table

    Args:
        num_books (integer):number of rows
    """
    database = r"C:\sqlite\db\library.db"
    conn = create_connection(database)
    for _ in range(num_books):
        history=generate_fake_user_history()
        history_values=[history['book_id']]
        history_id=create_new_user_history(conn, history_values)













