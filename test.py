import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from Main import suggestions, popular_books, borrow_book, return_book

class TestSuggestions(unittest.TestCase):

    @patch('Main.create_connection')
    @patch('pandas.read_sql_query')
    def test_suggestions(self, mock_read_sql_query, mock_create_connection):
        # Mock the database connection
        mock_conn = MagicMock()
        mock_create_connection.return_value = mock_conn
        mock_db=MagicMock()

        # Mock the dataframes
        mock_df = pd.DataFrame({
            'genre_id': [1, 1, 1, 3, 4],
            'name': ['Book1', 'Book2', 'Book3', 'Book4', 'Book5'],
            'book_id': [1, 2, 3, 4, 5]
        })
        mock_df_2 = pd.DataFrame({
            'genre_id': [1, 2, 3, 4, 5],
            'name': ['Book1', 'Book2', 'Book3', 'Book4', 'Book5'],
            'book_id': [1, 2, 3, 4, 5]
        })

        mock_read_sql_query.side_effect = [mock_df, mock_df_2]

        # Call the function with the mock database
        actual_result = suggestions(mock_db)
        
        # Expected dataframe
        expected_result = pd.DataFrame({
            'genre_id': [1],
            'name': ['Book1'],
            'book_id': [1]
        })

        # Reset indexes of each dataframe
        actual_result.reset_index(drop=True, inplace=True)
        expected_result.reset_index(drop=True, inplace=True)

        # Check the connection to database has been created
        mock_create_connection.assert_called_once_with(mock_db)

        # Check if the actual result is the same as the expected result
        pd.testing.assert_frame_equal(actual_result, expected_result)




    @patch('Main.create_connection')
    @patch('pandas.read_sql_query')
    def test_popular_books(self, mock_read_sql_query, mock_create_connection):
        # Mock the database connection
        mock_conn = MagicMock()
        mock_create_connection.return_value = mock_conn
        mock_db=MagicMock()

        # Mock the dataframes
        mock_df = pd.DataFrame({
            'review': [1, 2, 3, 5, 5, 3, 5, 1, 2, 4],
            'name': ['Book1', 'Book2', 'Book3', 'Book4', 'Book5', 'Book6', 'Book7', 'Book8','Book9','Book10'],
            'book_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        })

        mock_read_sql_query.side_effect = [mock_df]

        # Call the function with the mock database
        actual_result = popular_books(mock_db)

        # Expected dataframe
        expected_result=pd.DataFrame({
            'review': [5, 5, 5, 4, 3],
            'name': ['Book4', 'Book5', 'Book7', 'Book10', 'Book3'],
            'book_id': [4, 5, 7, 10, 3]
        })
        # Reset indexes of each dataframe
        actual_result.reset_index(drop=True, inplace=True)
        expected_result.reset_index(drop=True, inplace=True)

        # Check the connection to database has been created
        mock_create_connection.assert_called_once_with(mock_db)

        # Check if the actual result is the same as the expected result
        pd.testing.assert_frame_equal(actual_result, expected_result)




    @patch('Main.create_connection')
    @patch('pandas.read_sql_query')
    @patch('builtins.input', return_value='1')
    def test_borrow_book_available(self, mock_input, mock_read_sql_query, mock_create_connection):
        # Mock the database connection
        mock_conn = MagicMock()
        mock_create_connection.return_value = mock_conn
        mock_db=MagicMock()

        # Mock the dataframes
        mock_df = pd.DataFrame({
            'book_id': [1, 2, 3],
            'available': [1, 0, 0]
        })
        mock_df_history = pd.DataFrame({
            'id': [1, 2],
            'book_id': [2, 3]
        })
        mock_read_sql_query.side_effect = [mock_df, mock_df_history]

        # Call the function with the mock database
        borrow_book(mock_db)

        # Check the connection to database has been created
        mock_create_connection.assert_called_once_with(mock_db)

        # Check if the tables have been updated correctly
        pd.testing.assert_frame_equal(mock_df, pd.DataFrame({
            'book_id': [1, 2, 3],
            'available': [0, 0, 0]
        }))
        pd.testing.assert_frame_equal(mock_df_history, pd.DataFrame({
            'id': [1, 2, 3],
            'book_id': [2, 3, 1]
        }))


    @patch('Main.create_connection')
    @patch('pandas.read_sql_query')
    @patch('builtins.input', return_value='2')
    def test_borrow_book_unavailable(self, mock_input, mock_read_sql_query, mock_create_connection):
        # Mock the database connection
        mock_conn = MagicMock()
        mock_create_connection.return_value = mock_conn
        mock_db=MagicMock()

        # Mock the dataframes
        mock_df = pd.DataFrame({
            'book_id': [1, 2, 3],
            'available': [1, 0, 0]
        })
        mock_df_history = pd.DataFrame({
            'id': [1, 2],
            'book_id': [2, 3]
        })
        mock_read_sql_query.side_effect = [mock_df, mock_df_history]

        # Call the function with the mock database
        borrow_book(mock_db)

        # Check the connection to database has been created
        mock_create_connection.assert_called_once_with(mock_db)

        # Check if the tables have been updated correctly
        pd.testing.assert_frame_equal(mock_df, pd.DataFrame({
            'book_id': [1, 2, 3],
            'available': [1, 0, 0]
        }))
        pd.testing.assert_frame_equal(mock_df_history, pd.DataFrame({
            'id': [1, 2],
            'book_id': [2, 3]
        }))

    @patch('Main.create_connection')
    @patch('pandas.read_sql_query')
    @patch('builtins.input', return_value='1')
    def test_borrow_book_already_in_history(self, mock_input, mock_read_sql_query, mock_create_connection):
        # Mock the database connection
        mock_conn = MagicMock()
        mock_create_connection.return_value = mock_conn
        mock_db=MagicMock()

        # Mock the dataframes
        mock_df = pd.DataFrame({
            'book_id': [1, 2, 3],
            'available': [1, 0, 0]
        })
        mock_df_history = pd.DataFrame({
            'id': [1, 2],
            'book_id': [1, 3]
        })
        mock_read_sql_query.side_effect = [mock_df, mock_df_history]

        # Call the function with the mock database
        borrow_book(mock_db)

        # Check the connection to database has been created
        mock_create_connection.assert_called_once_with(mock_db)

        # Check if the tables have been updated correctly
        pd.testing.assert_frame_equal(mock_df, pd.DataFrame({
            'book_id': [1, 2, 3],
            'available': [0, 0, 0]
        }))
        pd.testing.assert_frame_equal(mock_df_history, pd.DataFrame({
            'id': [1, 2],
            'book_id': [1, 3]
        }))

    @patch('Main.create_connection')
    @patch('pandas.read_sql_query')
    @patch('builtins.input', return_value='1')
    def test_return_book(self, mock_input, mock_read_sql_query, mock_create_connection):
        # Mock the database connection
        mock_conn = MagicMock()
        mock_create_connection.return_value = mock_conn
        mock_db=MagicMock()

        # Mock the dataframes
        mock_df = pd.DataFrame({
            'book_id': [1, 2, 3],
            'available': [0, 1, 0]
        })

        mock_read_sql_query.side_effect = [mock_df]

        # Call the function with the mock database
        return_book(mock_db)

        # Check the connection to database has been created
        mock_create_connection.assert_called_once_with(mock_db)

        # Check if the tables have been updated correctly
        pd.testing.assert_frame_equal(mock_df, pd.DataFrame({
            'book_id': [1, 2, 3],
            'available': [1, 1, 0]
        }))


if __name__ == '__main__':
    unittest.main()