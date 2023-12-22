from database import *
from data import *
import os.path
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from database_classes import *

def create_connection(database_path):
    """ create a database connection to the database
        specified by database_path
    :param database_path: database file
    :return: Connection object or None
    """
    engine = create_engine(database_path, echo=True)
    return engine

def create_connection_sqlite(db_file):
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

def select_all_history(conn):
    """
    Query all rows in the books table
    :param conn: the Connection object
    :return:all availabily
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM history")

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


def initial_menu():
    """This function asking user to choose one of the options from the Menu

    Returns:
        The user's choice
    """
    while True:
        try:
            user_input=int(input("Choose on of the following options: \n1.Suggestions \n2.Popular books \n3.Borrow a book \n4.Return a book \n5.User History Stats: "))
            if user_input<6:
                return user_input
            else:
                print("You have to select between 1 and 5")
        except ValueError as e:
            print('You have to type a number')



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
    conn = create_connection_sqlite(database)
    #create a dataframe that contains books of the history table and their genres and names by the book table
    query = 'SELECT books.genre_id, books.name,history.book_id FROM books JOIN history ON books.id=history.book_id '
    df = pd.read_sql_query(query, conn)
    #Finds the favourite genre of the user by counting the books for each genre, and the max number in the column
    count=df.groupby('genre_id').size().reset_index(name='genre_count')
    find_max = count['genre_count'].idxmax()
    favourite_genre = count.loc[find_max, 'genre_count']
    #From the books table selects all the tables with the favourite genre of the user and displays the list of the books as suggestions
    query_2='SELECT * FROM books'
    df_2=pd.read_sql_query(query_2, conn)
    same_genre_books=df_2["genre_id"] == favourite_genre
    suggestions=df_2[same_genre_books]
    pd.set_option('display.max_columns', None)
    #close database connection
    conn.close()
    print(f'Below you can find our suggestions: \n{suggestions}')


def popular_books(database):
    """This function shows the first 5 books with the best reviews

    Args:
        database: the library database
    """
    #create database connection
    conn = create_connection_sqlite(database)
    #create the books table in dataframe
    query='SELECT * FROM books'
    df=pd.read_sql_query(query, conn)
    #finds the 5 largest from review column and displays all the columns
    top_5 = df.nlargest(5, "review")
    pd.set_option('display.max_columns', None)
    #close database connection
    conn.close()
    print(f'Current Top 5 books: \n{top_5}')


def search_book(database):
    """This function searches for the user's input in column "names"

    Args:
        database: the library database
    """
    #create database connection
    conn = create_connection_sqlite(database)
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
    If the book is available and it is the first time the user borrows it , adds the book on History

    Args:
        database: The library database
    """
    #create database connection
    conn=create_connection_sqlite(database)
    #create the availability table in dataframe
    query='SELECT * FROM availability'
    df = pd.read_sql_query(query, conn)
    #Prompt the user to input the book id
    while True:
        try:
            user_input = int(input("Type the book id of the book you want to borrow: "))
            #if book exists will check if it is available and if it is will make it unavailable
            if user_input in df['book_id'].values:
                if df.loc[df['book_id'] == user_input, 'available'].values[0]:
                    #book availabilty changes to unavailable
                    updated_availability=0
                    df.loc[df['book_id'] == user_input, 'available']=updated_availability
                    #updates the database
                    df.to_sql('availability', conn, if_exists='replace', index=False)
                    query_history='SELECT * FROM history'
                    df_history = pd.read_sql_query(query_history, conn)
                    #checks if the user has borrowed the book again
                    if user_input in df_history['book_id'].values:
                        print ('Book has been borrowed in the past')
                    else:
                        #adds the book in history if it is the first time that has been borrowed
                        df_history.loc[len(df_history.index)] =[len(df_history)+1, user_input]
                        df_history.to_sql('history', conn, if_exists='replace', index=False)
                    select_all_history(conn)
                    print("Book is ready to collect. Database has been updated")
                    break
                else:
                    print(f"Book id {user_input} is not available.")
                    print(df)
                    break
            else:
                    print("This book id doesn't exist")
        except ValueError as e:
            print(e)
            print('You have to type a book id')


def return_book(database):
    """This function checks if the book_id the user inputs exists,
    and if exists and is unavailble it makes it available and updates the database.

    Args:
        database: The library database
    """
    #create database connection
    conn=create_connection_sqlite(database)
    #create the availability table in dataframe
    query='SELECT * FROM availability'
    df = pd.read_sql_query(query, conn)
    #Prompt the user to input the book id
    while True:
        try:
            user_input = int(input("Type the book id of the book you want to return: "))
            #if book exists will check if it is unavailable and if it is will make it available
            if user_input in df['book_id'].values:
                if not df.loc[df['book_id'] == user_input, 'available'].values[0]:
                    #book availabilty changes to unavailable
                    updated_availability=1
                    df.loc[df['book_id'] == user_input, 'available']=updated_availability
                    #updates the database
                    df.to_sql('availability', conn, if_exists='replace', index=False)
                    select_all_availabily(conn)
                    print("Book has been returned. Database has been updated")
                    break
                else:
                    print(f"Book id exists. You have typed wrong book id.")
            else:
                print("This book id doesn't exist")
        except ValueError as e:
            print(e)
            print('You have to type a book id')

def user_history(database):
     #creates the database connection
    conn=create_connection_sqlite(database)
    #creates a query to bring all the genres user has read
    query='SELECT genres.genre FROM history JOIN books ON history.book_id=books.id JOIN genres ON books.genre_id=genres.id '
    df = pd.read_sql_query(query, conn)
    print(df)
    #creates a dataframe that counts the amount of books from each genre user read
    count=df.groupby('genre').size().reset_index(name='genre_total')
    #creates a bar plot with the genre stats
    sns.barplot(x='genre', y='genre_total', data=count,  hue="genre")
    plt.show()
    conn.close()



def add_data(database):
    insert_books(50,database)
    insert_availability(50,database)
    insert_authors(10,database)
    insert_genres(5,database)
    insert_user_history(10,database)
    print('Database has been updated')


def main():
    """Main function of library
    """
    # Checking if library exists. If exists a menu will display
    file_path= 'sqlite:///library.db'

    # Extract the file path from the connection string
    # The file path is everything after 'sqlite:///'
    # For example, 'sqlite:///library.db' becomes 'library.db'
    file_name = file_path.split('sqlite:///')[-1]

    if os.path.exists(file_name):
        selection=initial_menu()
        if selection==1:
            suggestions(file_name)
        elif selection==2:
            popular_books(file_name)
        elif selection==3:
            borrow_book(file_name)
        elif selection==4:
            return_book(file_name)
        else:
            user_history(file_name)

    # If the library doesn't exist it creates a new one
    else:
        try:
            Base.metadata.create_all(engine)
        except Error as e:
            print(e)
        print('Database has been created')
        add_data(file_path)
        selection=initial_menu()
        if selection==1:
            suggestions(file_name)
        elif selection==2:
            popular_books(file_name)
        elif selection==3:
            borrow_book(file_name)
        elif selection==4:
            return_book(file_name)
        else:
            user_history(file_name)




if __name__ == '__main__':
    main()