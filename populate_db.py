import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'Formula1.settings')

import django
django.setup()

from django.utils import timezone
from formula.models import *
from random import randint

# GENERIC FIELDS
GENERIC_DESC = "This object is created as part of populate_db.py testing. This description is generic and is the same for all object. Object should be deleted before deployment."
GENERIC_PASSWORD = "abcdefg"


def add_category(name, description, date_added, parent):
    c = Category.objects.get_or_create(name=name)[0]
    c.description = description
    c.date_added = date_added
    c.parent = parent
    c.save()
    return c

def add_topic(name, description, date_added, category):
    t = Topic.objects.get_or_create(category=category, name=name)[0]
    t.description = description
    t.date_added = date_added
    t.category = category
    t.save()
    return t

def add_post(title, description, content, file, viewership, date_added, topic, author):
    p = Post.objects.get_or_create(id=id)[0]
    pass

def add_user(username, email, password, student_id, first_name, last_name, bio, admin):
    u = User.objects.get_or_create(username=username)[0]
    u.email = email
    u.set_password(password)
    u.save()
    v = UserProfile.objects.get_or_create(user=u)[0]
    v.student_id = student_id
    v.first_name = first_name
    v.last_name = last_name
    v.bio = bio
    v.admin = admin
    v.save()
    return v


def create_objects():
    # Category - Software
    software = [
        {
            'name': 'Java',
            'description': GENERIC_DESC,
            'date_added': timezone.now(),
        },
        {
            'name': 'Python',
            'description': GENERIC_DESC,
            'date_added': timezone.now(),
        },
        {
            'name': 'C++',
            'description': GENERIC_DESC,
            'date_added': timezone.now(),
        }
    ]

    # Category - PR
    public_relations = [
        {
            'name': 'Finance',
            'description': GENERIC_DESC,
            'date_added': timezone.now(),
        },
        {
            'name': 'Marketing',
            'description': GENERIC_DESC,
            'date_added': timezone.now(),
        },
    ]

    # Category - Engineering Projects
    engineering_projects = [
        {
            'name': 'Aerodynamics',
            'description': GENERIC_DESC,
            'date_added': timezone.now(),
        },
        {
            'name': 'Chassis Design',
            'description': GENERIC_DESC,
            'date_added': timezone.now(),
        },
        {
            'name': 'Powertrain',
            'description': GENERIC_DESC,
            'date_added': timezone.now(),
        },
        {
            'name': 'Suspension',
            'description': GENERIC_DESC,
            'date_added': timezone.now(),
        },
        {
            'name': 'Electronics',
            'description': GENERIC_DESC,
            'date_added': timezone.now(),
        },
        {
            'name': 'Materials',
            'description': GENERIC_DESC,
            'date_added': timezone.now(),
        },
        {
            'name': 'Testing and Simulation',
            'description': GENERIC_DESC,
            'date_added': timezone.now(),
        },
    ]

    # Category - Design
    design = [
        {
            'name': 'Vehicle Design',
            'description': GENERIC_DESC,
            'date_added': timezone.now(),
        },
        {
            'name': 'Graphics Design',
            'description': GENERIC_DESC,
            'date_added': timezone.now(),
        },
    ]

    # Category - Business Operations
    business_operations = [
        {
            'name': 'Sponsorship',
            'description': GENERIC_DESC,
            'date_added': timezone.now(),
        },
        {
            'name': 'Event Management',
            'description': GENERIC_DESC,
            'date_added': timezone.now(),
        },
    ]

    categories_dict = {
        'Software': {
            'topics': software,
            'description': GENERIC_DESC,
            'date_added': timezone.now(),
            'parent': Category.GENERAL,
        },
        'Public Relations': {
            'topics': public_relations,
            'description': GENERIC_DESC,
            'date_added': timezone.now(),
            'parent': Category.OPERATION,
        },
        'Engineering Projects': {
            'topics': engineering_projects,
            'description': GENERIC_DESC,
            'date_added': timezone.now(),
            'parent': Category.EVEHICLE,
        },
        'Design': {
            'topics': design,
            'description': GENERIC_DESC,
            'date_added': timezone.now(),
            'parent': Category.GENERAL,
        },
        'Business Operations': {
            'topics': business_operations,
            'description': GENERIC_DESC,
            'date_added': timezone.now(),
            'parent': Category.OPERATION,
        },
    }

    return categories_dict
   


def create_dummy_categories():
    categories_dict = {}
    
    def generate_cd(cat_name, cat_parent):
        categories_dict[cat_name] = {'description':GENERIC_DESC,
                                     'date_added':timezone.now(),
                                     'parent':cat_parent,}

    generate_cd('Engineering Projects', Category.EVEHICLE)
    generate_cd('Software Development', Category.EVEHICLE)
    generate_cd('Design', Category.GENERAL)
    generate_cd('Business Operations', Category.OPERATION)
    generate_cd('Research and Development', Category.EVEHICLE)
    generate_cd('Testing', Category.EVEHICLE)
    generate_cd('Marketing', Category.OPERATION)
    generate_cd('Finance', Category.OPERATION)
    generate_cd('Events', Category.OPERATION)
    generate_cd('Education', Category.GENERAL)
    generate_cd('Community Outreach', Category.OPERATION)

    return categories_dict


def create_dummy_topics(categories_dict:dict):
    for category in categories_dict:
        topic_list = []

    def dummy_topic(topic_name, category):
        topic = {
                    'name':topic_name,
                    'description':GENERIC_DESC,
                    'date_added':timezone.now(),
                    'category':category,
                }
        return topic

def test_add_user():
    add_user(username='bobbykeren', 
             email='bob@gmail.com', 
             password=GENERIC_PASSWORD, 
             student_id=2773789, 
             first_name='Bob', 
             last_name='Keren', 
             bio=GENERIC_DESC, 
             admin=False)
    print(f'USER add succesful - Bob')



def populate():
    cats = create_objects()

    for cat, cat_data in cats.items():
        category = add_category(cat, cat_data['description'], cat_data['date_added'], cat_data['parent'])
        for topic in cat_data['topics']:
            add_topic(topic['name'], topic['description'], topic['date_added'], category)


    # Print out the categories we have added.
    for category in Category.objects.all():
        for topic in Topic.objects.filter(category=category):
            print(f'CATEGORY:TOPIC add succesful - {category}: {topic}')


# Start execution here!
if __name__ == '__main__':
    print('Starting Formula1 population script...')
    #populate()
    test_add_user()