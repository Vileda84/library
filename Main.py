from database import *
from data import *
import os.path
import pandas as pd
import numpy as np

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


def initial_menu():
    """Asks user to choose one of the options below:
    1.Suggestions
    2.Popular books
    3.Borrow a book
    4.User History Stats

    Raises:
        ValueError: For numbers >5

    Returns:
        int: the selection of the user
    """
    user_input=int(input("Choose on of the following options: \n1.Suggestions \n2.Popular books \n3.Search \n4.User History Stats: "))
    if user_input>4:
        raise ValueError('You must choose one selection between 1 and 4')
    return user_input

def summaries(database):
    conn = create_connection(database)
    table_name = 'books'
    column_name = 'summary'
    query = f'SELECT {column_name} FROM {table_name}'
    df = pd.read_sql_query(query, conn)
    conn.close()
    print(df)

def suggestions(database):
    """Finds the favourite genre of the user from the history table
    and filters the books on books table by this category in order to show suggestions
    that user will like

    Args:
        database: the library database
    """
    #create database connection
    conn = create_connection(database)
    #create a dataframe that contains books of the history table and their genres and names by the book table
    query = 'SELECT books.genre_id, books.name,history.book_id FROM books JOIN history ON books.id=history.book_id '
    df = pd.read_sql_query(query, conn)
    print (df)
    #Finds the favourite genre of the user by counting the books for each genre, and the max number in the column
    count=df.groupby('genre_id').size().reset_index(name='genre_count')
    find_max = count['genre_count'].idxmax()
    favourite_genre = count.loc[find_max, 'genre_count']
    print(favourite_genre)
    #From the books table selects all the tables with the favourite genre of the user and displays the list of the books as suggestions
    query_2='SELECT * FROM books'
    df_2=pd.read_sql_query(query_2, conn)
    same_genre_books=df_2["genre_id"] == favourite_genre
    suggestions=df_2[same_genre_books]
    #close database connection
    conn.close()
    print(suggestions)


def popular_books(database):
    """This function shows the first 5 books with the best reviews

    Args:
        database: the library database
    """
    #create database connection
    conn = create_connection(database)
    #create the books table in dataframe
    query='SELECT * FROM books'
    df=pd.read_sql_query(query, conn)
    #finds the 5 largest from review column and displays all the columns
    top_5 = df.nlargest(5, "review")
    pd.set_option('display.max_columns', None)
    #close database connection
    conn.close()
    print(top_5)


def search_book(database):
    """This function searches for the user's input in column "names"

    Args:
        database: the library database
    """
    #create database connection
    conn = create_connection(database)
    #create the books table in dataframe
    query='SELECT * FROM books'
    df=pd.read_sql_query(query, conn)
    while True:
        #user input
        user_input=(input("Find a book: "))
        #search for the user input in name column
        results=df[df['name'].str.contains(user_input, case=False)]
        if not results.empty:
            pd.set_option('display.max_columns', None)
            print(results)
            break
        else:
            print("The book doesn't exist")
        #close database connection
    conn.close()


def borrow_book(database):
    """This function checks if the book_id the user inputs exists,
    and if exists and is available it makes it unavailable.

    Args:
        database: The library database
    """
    #create database connection
    conn=create_connection(database)
    #create the availability table in dataframe
    query='SELECT * FROM availability'
    df = pd.read_sql_query(query, conn)
    #Prompt the user to input the book id
    while True:
        user_input = int(input("Type the book id of the book you want to borrow: "))
        #if book exists will check if it is available and if it is will make it unavailable
        if user_input in df['book_id'].values:
            if df.loc[df['book_id'] == user_input, 'available'].values[0]:
                #book availabilty changes to unavailable
                updated_availability=0
                df.loc[df['book_id'] == user_input, 'available']=updated_availability
                #updates the database
                df.to_sql('availability', conn, if_exists='replace')
                select_all_availabily(conn)
                print("Book is ready to collect. Database has been updated")
                break
            else:
                print(f"Book id {user_input} is not available.")
                break
        else:
            print("This book id doesn't exist")
    conn.close()

def return_book(database):
    """This function checks if the book_id the user inputs exists,
    and if exists and is unavailble it makes it available and updates the database.

    Args:
        database: The library database
    """
    #create database connection
    conn=create_connection(database)
    #create the availability table in dataframe
    query='SELECT * FROM availability'
    df = pd.read_sql_query(query, conn)
    #Prompt the user to input the book id
    while True:
        user_input = int(input("Type the book id of the book you want to return: "))
        #if book exists will check if it is unavailable and if it is will make it available
        if user_input in df['book_id'].values:
            if not df.loc[df['book_id'] == user_input, 'available'].values[0]:
                #book availabilty changes to unavailable
                updated_availability=1
                df.loc[df['book_id'] == user_input, 'available']=updated_availability
                #updates the database
                df.to_sql('availability', conn, if_exists='replace')
                select_all_availabily(conn)
                print("Book has been returned. Database has been updated")
                break
            else:
                print(f"Book id exists. You have typed wrong book id.")
        else:
            print("This book id doesn't exist")
    conn.close()




def add_data():
    insert_books(50)
    insert_availability(50)
    insert_authors(10)
    insert_genres(5)
    insert_user_history(10)
    print('Database has been updated')


def main():
    """Main function of library
    """
    # Checking if library exists. If exists a menu will display
    file_path="C:\sqlite\db\library.db"
    if os.path.exists(file_path):
        first_selection=initial_menu()
        return_book(file_path)

    # If the library doesn't exist it creates a new one
    else:
        try:
            create_database(file_path)
        except Error as e:
            print(e)
        print('Database has been created')
        add_data()
        first_selection=initial_menu()
        print(first_selection)



if __name__ == '__main__':
    main()