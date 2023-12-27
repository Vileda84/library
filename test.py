import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from Main import suggestions, popular_books

class TestSuggestions(unittest.TestCase):

    @patch('Main.create_connection_sqlite')
    @patch('pandas.read_sql_query')
    def test_suggestions(self, mock_read_sql_query, mock_create_connection_sqlite):
        # Mock the database connection
        mock_conn = MagicMock()
        mock_create_connection_sqlite.return_value = mock_conn
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
        expected_result = pd.DataFrame({
            'genre_id': [1],
            'name': ['Book1'],
            'book_id': [1]
        })

        actual_result.reset_index(drop=True, inplace=True)
        expected_result.reset_index(drop=True, inplace=True)

        # Check if the actual result is the same as the expected result
        pd.testing.assert_frame_equal(actual_result, expected_result)


        # Check if the function calls are correct
        mock_create_connection_sqlite.assert_called_once_with(mock_db)


        # Check if the function closes the connection
        mock_conn.close.assert_called_once()

    @patch('Main.create_connection_sqlite')
    @patch('pandas.read_sql_query')
    def test_popular_books(self, mock_read_sql_query, mock_create_connection_sqlite):
        # Mock the database connection
        mock_conn = MagicMock()
        mock_create_connection_sqlite.return_value = mock_conn
        mock_db=MagicMock()

        mock_df = pd.DataFrame({
            'review': [1, 2, 3, 5, 5, 3, 5, 1, 2, 4],
            'name': ['Book1', 'Book2', 'Book3', 'Book4', 'Book5', 'Book6', 'Book7', 'Book8','Book9','Book10'],
            'book_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        })

        mock_read_sql_query.side_effect = [mock_df]
        actual_result = popular_books(mock_db)
        expected_result=pd.DataFrame({
            'review': [5, 5, 5, 4, 3],
            'name': ['Book4', 'Book5', 'Book7', 'Book10', 'Book3'],
            'book_id': [4, 5, 7, 10, 3]
        })

        actual_result.reset_index(drop=True, inplace=True)
        expected_result.reset_index(drop=True, inplace=True)

        # Check if the actual result is the same as the expected result
        pd.testing.assert_frame_equal(actual_result, expected_result)


        # Check if the function calls are correct
        mock_create_connection_sqlite.assert_called_once_with(mock_db)


        # Check if the function closes the connection
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()