import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'Formula1.settings')

import django
django.setup()

from django.utils import timezone
from formula.models import *

GENERIC_DESC = "This object is created as part of populate_db.py testing. This description is generic and is the same for all object. Object should be deleted before deployment."

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


def create_objects():

    # Category - software
    software = [
        {
            'name':'Java',
            'description':GENERIC_DESC,
            'date_added':timezone.now(),
        },
        {
            'name':'Python',
            'description':GENERIC_DESC,
            'date_added':timezone.now(),
        },
        {
            'name':'C++',
            'description':GENERIC_DESC,
            'date_added':timezone.now(),
        }
    ]

    # Category - PR
    public = [
        {
            'name':'Finance',
            'description':GENERIC_DESC,
            'date_added':timezone.now(),
        },
        {
            'name':'Marketing',
            'description':GENERIC_DESC,
            'date_added':timezone.now(),
        },
    ]
    
    categories_dict = {'Software':{'topics':software,
                                   'description':GENERIC_DESC,
                                   'date_added':timezone.now(),
                                   'parent':Category.EVEHICLE,
                                   },
                        'Public':{'topics':public,
                                  'description':GENERIC_DESC,
                                  'date_added':timezone.now(),
                                  'parent':Category.OPERATION
                                  },
                    }
    
    return categories_dict

def populate():
    cats = create_objects()

    for cat, cat_data in cats.items():
        category = add_category(cat, cat_data['description'], cat_data['date_added'], cat_data['parent'])
        for topic in cat_data['topics']:
            add_topic(topic['name'], topic['description'], topic['date_added'], category)


    # Print out the categories we have added.
    for category in Category.objects.all():
        for topic in Topic.objects.filter(category=category):
            print(f'- {category}: {topic}')


# Start execution here!
if __name__ == '__main__':
    print('Starting Formula1 population script...')
    populate()