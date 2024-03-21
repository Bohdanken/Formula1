import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'Formula1.settings')

import django
django.setup()

from django.utils import timezone
from random import randint
from formula.models import *
from population.randomdatetime import random_datetime

from db_dummy import *
