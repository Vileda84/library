from database import *
from data import *

database = r"C:\sqlite\db\library.db"
conn = create_connection(database)
def select_all_books(conn):
    """
    Query all rows in the books table
    :param conn: the Connection object
    :return:all books
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def select_all_availabily(conn):
    """
    Query all rows in the books table
    :param conn: the Connection object
    :return:all availabily
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM availability")

    rows = cur.fetchall()

    for row in rows:
        print(row)



def select_all_authors(conn):
    """
    Query all rows in the authors table
    :param conn: the Connection object
    :return:all authors
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM authors")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def select_all_genres(conn):
    """
    Query all rows in the genres table
    :param conn: the Connection object
    :return:all genres
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM genres")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def select_all_user_history(conn):
    """
    Query all rows in the genres table
    :param conn: the Connection object
    :return:all genres
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM history")

    rows = cur.fetchall()

    for row in rows:
        print(row)



def main():
    insert_books(50)
    insert_availability(50)
    insert_authors(10)
    insert_genres(5)
    insert_user_history(10)
    select_all_books(conn)
    select_all_availabily(conn)
    select_all_authors(conn)
    select_all_genres(conn)
    select_all_user_history(conn)


if __name__ == '__main__':
    main()