import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'Formula1.settings')

import django

django.setup()

from django.utils import timezone
from formula.models import *
from db_dummy import *

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
    try:
        cat = Category.objects.get(name=category)
    except Category.DoesNotExist:
        print(f'Category {category} does not exist for TOPIC: {name}.')
        return None
    t = Topic.objects.get_or_create(category=cat, name=name)[0]
    t.description = description
    t.date_added = date_added
    t.category = category
    t.save()
    return t


def add_post(title, description, content, file, viewership, date_added, topic, author):
    p = Post.objects.get_or_create(id=id)[0]
    pass



def add_user(username, email, password, student_id, first_name, last_name, bio, is_admin):
    user = add_user_only(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
    profile = add_user_profile(username=username, student_id=student_id, bio=bio, is_admin=is_admin)
    return profile


def add_user_only(username, email, password, first_name, last_name):
    user = User.objects.get_or_create(username=username)[0]
    user.email = email
    user.set_password(password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return user


def add_user_profile(username, student_id, bio, is_admin):
    try:
        user = User.objects.get(username=username)
        user_p = UserProfile.objects.get_or_create(user=user)
        if user_p[1] is False:
            print(f'User {username} already added')
            return user_p[0]
        else:
            user_p = user_p[0]
        user_p.student_id = student_id
        user_p.bio = bio
        user_p.is_admin = is_admin
        user_p.save()
        return user_p

    except User.DoesNotExist:
        print(f'USER {username} is not found in the database.')
        return None


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
        categories_dict[cat_name] = {'name': cat_name,
                                     'description': GENERIC_DESC,
                                     'date_added': timezone.now(),
                                     'parent': cat_parent,
                                     }

    for category, parent in CategoryDummy.CATEGORIES:
        generate_cd(category, parent)

    return categories_dict


def create_dummy_topics():
    topics_dict = {}

    def generate_td(topic_name, category):
        topics_dict[topic_name] = {'name': topic_name,
                                   'description': GENERIC_DESC,
                                   'date_added': timezone.now(),
                                   'category': category,
                                   }

    for topic, category in TopicDummy.TOPICS:
        generate_td(topic, category)

    return topics_dict


def assign_topics_to_categories(categories_dict: dict, topics_dict: dict):
    for topic in topics_dict:
        category = topics_dict[topic]['categories']
        if not 'topics' in categories_dict[category]:
            categories_dict[category]['topics'] = []
        categories_dict[category]['topics'].append(topics_dict[topic])

    return categories_dict


def create_dummy_user():
    for user in UserDummy.USERS:
        username = user['username']
        add_user(username=username,
                 email=user['email'],
                 password=GENERIC_PASSWORD,
                 first_name=user['first_name'],
                 last_name=user['last_name'],
                 student_id=UserProfileDummy.USER_PROFILE[username]['student_id'],
                 bio=GENERIC_DESC,
                 is_admin=False
                 )
        print(f'PROFILE add succesful - {username}')


def test_add_category():
    test_category = add_category(name='Test Category',
                                 description=GENERIC_DESC,
                                 date_added=timezone.now(),
                                 parent=Category.GENERAL
                                 )
    print(f'CATEGORY add succesful - Test Category')
    return test_category


def test_add_topic(category: Category):
    test_topic = add_topic(name='Fake Topic',
                           description=GENERIC_DESC,
                           date_added=timezone.now(),
                           category=category
                           )
    print(f'TOPIC add succesful - Fake Topic in {category.name}')
    return test_topic


def test_add_user():
    test_user = add_user(username='normaluser',
                         email='noadmin@privileges.com',
                         password=GENERIC_PASSWORD,
                         first_name='Normal',
                         last_name='User',
                         student_id=1111111,
                         bio='This is a generic user with no privileges',
                         is_admin=False
                         )
    print(f'USER add succesful - normaluser')
    return test_user


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


def dummy_populate():
    categories_dict = create_dummy_categories()
    for cat, cat_data in categories_dict.items():
        added_category = add_category(cat_data['name'], cat_data['description'], cat_data['date_added'],
                                      cat_data['parent'])
        print(f'CATEGORY add succesful - {added_category}')

    topics_dict = create_dummy_topics()
    for topic, top_data in topics_dict.items():
        added_topic = add_topic(top_data['name'], top_data['description'], top_data['date_added'], top_data['category'])
        print(f'TOPIC add succesful - {added_topic} in {added_topic.category}')

    profiles_dict = create_dummy_user()


# Start execution here!
if __name__ == '__main__':
    print('Starting Formula1 population script...')
    t_user = test_add_user()
    t_category = test_add_category()
    t_topic = test_add_topic(t_category)
    dummy_populate()
