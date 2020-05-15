#!/usr/bin/env python
import csv
'''
import os

import sys

def launchServer():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(['manage.py','runserver','192.168.0.188:8000'])
launchServer()
'''



with open('downloaded_models.csv', newline='') as csvfile:
         print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
         spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
         for row in spamreader:
             print(row)
