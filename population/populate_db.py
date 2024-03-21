from population.setup import *
from population.dummy_populate import dummy_populate
from population.testadd import run_test

def populate():
    run_test(resetafter=True)
    print('Starting to populate Formula1...')
    print("----------------- POPULATION---------------------------------------------------------------")
    dummy_populate()
    print("----------------- POPULATION SUCCESS ------------------------------------------------------")