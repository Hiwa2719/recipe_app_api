from django.db.utils import OperationalError
from django.core.management import call_command
from django.test import TestCase
from unittest.mock import patch


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """waiting for db when db is ready"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """testing wait for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
