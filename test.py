import select
import unittest
from unittest.mock import patch
import mock
from sqlalchemy import MetaData, create_engine, Table
from faker import Faker
from sqlalchemy.orm import sessionmaker
from data import generate_fake_book, insert_books
import database_classes

class TestGenerateFakeBook(unittest.TestCase):
    @patch('data.Faker')
    @patch('data.random')
    def test_generate_fake_book(self, mock_random, mock_faker):
        # Mocking random and Faker to control the generated fake data
        fake_instance = mock_faker.return_value
        mock_random.randint.side_effect = [56, 3, 2, 1]

        # Calling the function
        result = generate_fake_book()

        # Asserting the result
        self.assertIsNotNone(result)
        self.assertEqual(result.name, 'book56')
        self.assertEqual(result.isbn, fake_instance.isbn10.return_value)  # No change here, using the actual value generated by fake.isbn10()
        self.assertEqual(result.author_id, 3)
        self.assertEqual(result.genre_id, 2)
        self.assertEqual(result.review, 1)

        # Asserting that random.randint was called with the expected arguments
        mock_random.randint.assert_has_calls([mock.call(1, 100), mock.call(1, 10), mock.call(1, 5)])



if __name__ == '__main__':
    unittest.main()