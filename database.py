import sqlite3
from sqlite3 import Error

# https://www.sqlitetutorial.net/sqlite-python/creating-tables/

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_new_book(conn, book):
    """
    Create a new book into the books table
    :param conn:
    :param book:
    :return: book id
    """
    sql = ''' INSERT INTO books(name,isbn,author_id,genre_id, summary, review)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql,book)
    conn.commit()
    return cur.lastrowid

def create_new_availability(conn, availability):
    """
    Create a new availability into the availability table
    :param conn:
    :param availability:
    :return: availability id
    """
    sql = ''' INSERT INTO availability(book_id,available)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, availability)
    conn.commit()
    return cur.lastrowid


def create_new_author(conn, author):
    """
    Create a new author into the authors table
    :param conn:
    :param author:
    :return: author id
    """
    sql = ''' INSERT INTO authors(first_name, last_name)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, author)
    conn.commit()
    return cur.lastrowid


def create_new_genre(conn, genre):
    """
    Create a new genre into the genres table
    :param conn:
    :param genre:
    :return: genre id
    """
    sql = ''' INSERT INTO genres(name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, genre)
    conn.commit()
    return cur.lastrowid

def create_new_user_history(conn, history):
    """
    Create a new history into the user_history table
    :param conn:
    :param history:
    :return: history id
    """
    sql = ''' INSERT INTO history(book_id)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, history)
    conn.commit()
    return cur.lastrowid



def create_database(database):


#Create Book Table>Book ID, Book name, ISBN ,AuthorID, Genre ID

    sql_create_books_table = """ CREATE TABLE IF NOT EXISTS books (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        isbn text NOT NULL,
                                        author_id integer NOT NULL,
                                        genre_id integer NOT NULL,
                                        summary text NOT NULL,
                                        review integer NOT NULL,
                                        FOREIGN KEY (author_id) REFERENCES authors (id),
                                        FOREIGN KEY (genre_id) REFERENCES genres (id)
                                    ); """

#Create Availability > Book ID, Availability ID, User ID, Is it available

    sql_create_availability_table = """ CREATE TABLE IF NOT EXISTS availability (
                                        id integer PRIMARY KEY,
                                        book_id integer NOT NULL,
                                        available boolean NOT NULL,
                                        FOREIGN KEY (book_id) REFERENCES books (id)
                                    ); """


#User Profile > User ID, First Name, Last Name

    sql_create_user_history_table = """ CREATE TABLE IF NOT EXISTS history (
                                        id integer PRIMARY KEY,
                                        book_id integer NOT NULL,
                                        FOREIGN KEY (book_id) REFERENCES books (id)
                                    ); """


#Author Table > Author ID ,First Name, Last Name
    sql_create_authors_table = """ CREATE TABLE IF NOT EXISTS authors (
                                        id integer PRIMARY KEY,
                                        first_name text NOT NULL,
                                        last_name text NOT NULL
                                    ); """

#Gentre> Gentre ID, Gentre name
    sql_create_genres_table = """ CREATE TABLE IF NOT EXISTS genres (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL
                                    ); """

 # create a database connection
    conn = create_connection(database)


# create tables
    if conn is not None:

        # create books table
        create_table(conn, sql_create_books_table)

        # create availability table
        create_table(conn, sql_create_availability_table)

        # create users table
        create_table(conn, sql_create_user_history_table)

        # create authors table
        create_table(conn, sql_create_authors_table)

        # create genres table
        create_table(conn, sql_create_genres_table)


    else:
        print("Error! cannot create the database connection.")




