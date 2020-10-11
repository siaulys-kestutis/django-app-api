# this will allow to mock the behaviour of the django get database function
# can use this to simulate the Db being available // NOT being available
from unittest.mock import patch

# allows to call the command in the source code
from django.core.management import call_command

# import the operational error that Django throws when the DB is NOT
# available;
# will USE THIS ERROR to simulate the DB being available or NOT
from django.db.utils import OperationalError
from django.test import TestCase

class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is ready"""
        # here need to simulate the behaviour of Django when the DB
        # is available

        # implemented management command will try to retrieve
        # the db connection from Django
        # if retrieves OperationalError - the DB is NOT available
        # if OperationalError is NOT thrown - the DB is available and the
        # command will continue

        # to simulate the test, override the behaviour of the
        # connection handler to return true to simulate the success

        # will use PATCH to mock the connection handler to just return
        # true every time it is called

        #'django.db.utils.ConnectionHandler.__getitem__' is the Django
        # function call for retrieving the DB
        # gi here now represents the __get_item__ command
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # this means that whenever 'django.db.utils.ConnectionHandler.__getitem__'
            # is called during the test execution, instead performing
            # the expected Django behaviour, it will override it and
            # will replace it with a mock object which:
            # - returns the specified value
            # - allows to monitor how many times the patched command
            # was called, and different calls that were made to it
            gi.return_value = True
            # 'wait_for_db' is the name of the management command
            call_command('wait_for_db')
            # check that gi was called once
            self.assertEqual(gi.call_count, 1)

    # PATCH DECORATOR
    # patch replaces the behaviour of time.sleep with the function
    # that returns True
    # this is just to speed up the test
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for DB"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # the first five times one calls the __get_item
            # they will get an operational error
            # on the sixth time, it will return True
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            # assert the function got called 6 times
            self.assertEqual(gi.call_count, 6)


