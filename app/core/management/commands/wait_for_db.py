import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until the Db is available"""

    # the arguments can be passed to, say, modify the wait time of the
    # function
    def handle(self, *args, **options):
        """
        From the BaseCommand docs:
        The actual logic of the command. Subclasses must implement
        this method.
        """
        self.stdout.write('Waiting for database...')
        db_conn = None
        # while db_conn is a 'falsy value': false, blank string, none
        while not db_conn:
            try:
                # try and set the db_conn to the database connection
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1s...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))
