import crud
import unittest
import doctest
import os
from model import db, User, Inventory, Item, connect_to_db


os.system('dropdb capstonetest')
os.system('createdb capstonetest')

class MyAppUnitTestCase(unittest.TestCase):

    def test_create_user(self):
        """Test create_user function by checking if instance returned is User."""
        user = crud.create_user(email='test1@test.com', password='test')
        self.assertIsInstance(user, User)

if __name__ == '__main__':
    from server import app
    connect_to_db(app, 'capstonetest')
    with app.app_context():
        db.create_all()

    unittest.main()