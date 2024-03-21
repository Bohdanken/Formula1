from population.setup import *
from population.add import *
from population.create import *
from population.save import *
from population.dummy_populate import dummy_populate
from population.testadd import run_test

def populate():
    run_test(resetafter=True)
    dummy_populate()