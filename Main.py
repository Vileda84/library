from database import *
from data import *
import os.path
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from database_classes import *

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



def suggestions(database):
    """Finds the favourite genre of the user from the history table
    and filters the books on books table by this category in order to show suggestions
    that user will like

    Args:
        database: the library database
    """
    # Create database connection
    conn = create_connection_sqlite(database)

    # Create a dataframe that contains books of the history table and their genres and names by the book table
    query = 'SELECT books.genre_id, books.name,history.book_id FROM books JOIN history ON books.id=history.book_id '

    # Creates a dataframe from the query
    df = pd.read_sql_query(query, conn)

    # Groups rows by gentre_id , finds the number of the rows and reset the index and renaming size as gentre_count
    count=df.groupby('genre_id').size().reset_index(name='genre_count')
    print(count)

    # Shows the row with the max number
    find_max = count['genre_count'].idxmax()
    print(find_max)
    # Retrieves the row
    favourite_genre = count.loc[find_max, 'genre_id']

    #From the books table selects all books
    query_2='SELECT * FROM books'

    # Creates a dataframe from the query
    df_2=pd.read_sql_query(query_2, conn)

    # Filters the dataframe in order to show the rows that are equal with favourite_genre
    suggestions=df_2[df_2["genre_id"] == favourite_genre]
    pd.set_option('display.max_columns', None)

    # Close database connection
    conn.close()

    # Prints suggestions
    #print(f'Below you can find our suggestions: \n{suggestions}')
    return suggestions


def popular_books(database):
    """This function shows the first 5 books with the best reviews

    Args:
        database: the library database
    """
    # Create database connection
    conn = create_connection_sqlite(database)

    # Create the books table in dataframe
    query='SELECT * FROM books'
    df=pd.read_sql_query(query, conn)

    # Finds the 5 largest from review column and displays all the columns
    top_5 = df.nlargest(5, "review")
    print(top_5)
    pd.set_option('display.max_columns', None)

    # Close database connection
    conn.close()
    return top_5



def borrow_book(database):
    """This function checks if the book_id the user inputs exists,
    and if exists and is available it makes it unavailable.
    If the book is available and it is the first time the user borrows it , adds the book on History

    Args:
        database: The library database
    """
    # Create database connection
    conn=create_connection_sqlite(database)
    # Create the availability table in dataframe
    query='SELECT * FROM availability'
    df = pd.read_sql_query(query, conn)

    # Prompt the user to input the book id
    while True:
        try:
            user_input = int(input("Type the book id of the book you want to borrow: "))
            # If book exists will check if it is available and if it is will make it unavailable
            if user_input in df['book_id'].values:
                # Locates the row with the book_id user has typed and retrieves the value of the first row in availability column
                if df.loc[df['book_id'] == user_input, 'available'].values[0]:

                    # Book availabilty changes to unavailable
                    updated_availability=0
                    df.loc[df['book_id'] == user_input, 'available']=updated_availability

                    # Updates the database
                    df.to_sql('availability', conn, if_exists='replace', index=False)

                    # Creates dataframe from History table
                    query_history='SELECT * FROM history'
                    df_history = pd.read_sql_query(query_history, conn)

                    # Checks if the user has borrowed the book again
                    if user_input in df_history['book_id'].values:
                        print ('Book has been borrowed in the past')
                    else:
                        # Adds the book in history if it is the first time that has been borrowed
                        df_history.loc[len(df_history.index)] =[len(df_history)+1, user_input]
                        df_history.to_sql('history', conn, if_exists='replace', index=False)
                    print("Book is ready to collect. Database has been updated")
                    break
                else:
                    # Prints that the book is not available
                    print(f"Book id {user_input} is not available.")
                    break
            else:
                    # If the book_id doesn't exist prints that doesn't exist
                    print("This book id doesn't exist")
        # Prints a ValueError if user types something wrong
        except ValueError as e:
            print(e)
            print('You have to type a book id')


def return_book(database):
    """This function checks if the book_id the user inputs exists,
    and if exists and is unavailble it makes it available and updates the database.
    If it available that means that the user has typed a wrong book_id

    Args:
        database: The library database
    """
    # Create database connection
    conn=create_connection_sqlite(database)

    # Create the availability table in dataframe
    query='SELECT * FROM availability'
    df = pd.read_sql_query(query, conn)

    # Prompt the user to input the book id
    while True:
        try:
            user_input = int(input("Type the book id of the book you want to return: "))

            # If book exists will check if it is unavailable and if it is will make it available
            if user_input in df['book_id'].values:

                # Locates the row with the book_id user has typed and retrieves the value of the first row in availability column
                if not df.loc[df['book_id'] == user_input, 'available'].values[0]:

                    # Book availabilty changes to anavailable
                    updated_availability=1
                    df.loc[df['book_id'] == user_input, 'available']=updated_availability

                    # Updates the database
                    df.to_sql('availability', conn, if_exists='replace', index=False)

                    # Prints that Book has been returned and database been updated
                    print("Book has been returned. Database has been updated")
                    break
                else:
                    # If the book is available prints the user typed the wrong book_id
                    print(f"Book id exists. You have typed wrong book id.")
            else:
                print("This book id doesn't exist")
        # Prints a ValueError if user types something wrong
        except ValueError as e:
            print(e)
            print('You have to type a book id')

def user_history(database):
    # Creates the database connection
    conn=create_connection_sqlite(database)

    # Creates a datatframe from a query to bring all the genres user has read
    query='SELECT genres.genre FROM history JOIN books ON history.book_id=books.id JOIN genres ON books.genre_id=genres.id '
    df = pd.read_sql_query(query, conn)
    print(df)

    # Groups rows by gentre , finds the number of the rows and reset the index and renaming size as gentre_total
    count=df.groupby('genre').size().reset_index(name='genre_total')

    # Creates a bar plot with the genre stats
    sns.barplot(x='genre', y='genre_total', data=count,  hue="genre")
    plt.show()
    conn.close()



def add_data(database):
    """Inserts all the data on the created tables

    Args:
        database: The library database
    """
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
    file_name = file_path.split('sqlite:///')[-1]

    # If file exist shows the initial menu
    if os.path.exists(file_name):
        selection=initial_menu()
        # Checks what input user typed and runs the selection
        if selection==1:
            print(f'Below you can find our suggestions: \n{suggestions(file_name)}')
        elif selection==2:
            print(f'Current Top 5 books: \n{popular_books(file_name)}')
        elif selection==3:
            borrow_book(file_name)
        elif selection==4:
            return_book(file_name)
        else:
            user_history(file_name)

    # If the library doesn't exist it creates a new one
    else:
        try:
            # Creates tables
            Base.metadata.create_all(engine)
            print('Database has been created')

            #Adds data
            add_data(file_path)

            selection=initial_menu()

            # Checks what input user typed and runs the selection
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
        except Error as e:
            print(e)



if __name__ == '__main__':
    main()