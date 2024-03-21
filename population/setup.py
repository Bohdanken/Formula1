import json

f = open('population/dummy_data.json')

data = json.load(f)

def no_of_entries():
    print('====================== DATA OVERVIEW ===========================')
    print(f'Number of entry(ies) for {len(data)-1} model(s):')
    line = 1
    total = 0
    for key, det in data.items():
        if line == 1:
            line += 1
            continue
        total += len(det)
        print(f'\t{key:<13}: {len(det):>5}')
    
    print()
    print(f'This population will add a total amount of {total} entries.')
    print()

def is_proceed():
    while True:
        response = input("  Proceed with population script?\n   Type 'yes' to continue, or 'no' to cancel: ")
        if (response == 'yes' or response == 'y'):
            print("Population proceed.")
            break
        elif (response == 'no' or response == 'n'):
            print("Population cancelled.")
            exit()
        else:
            print("Invalid response.")


# Running point
no_of_entries()
is_proceed()


import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'Formula1.settings')

import django
django.setup()

from django.utils import timezone
from random import randint
from formula.models import *
from population.randomdatetime import random_datetime

