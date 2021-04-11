import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to pause execution until database is available"""
    def handle(self, *args, **options):
        """when we enter the command this method will be called"""
        self.stdout.write('Waiting for database .... ')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting one second ...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database is available now!'))
