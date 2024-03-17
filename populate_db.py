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


def add_topic(name, description, date_added, category_name):
    try:
        category = Category.objects.get(name=category_name)
    except Category.DoesNotExist:
        print(f'Category {category_name} does not exist for TOPIC: {name}.')
        return None
    t = Topic.objects.get_or_create(category=category, name=name)[0]
    t.description = description
    t.date_added = date_added
    t.category = category_name
    t.save()
    return t


def add_post(title, description, content, viewership, date_added, topic_name, author_username):
    try:
        topic = Topic.objects.get(name=topic_name)
        author = User.objects.get(username=author_username)
    except Topic.DoesNotExist:
        print(f'Topic {topic_name} does not exist for POST: {title}.')
        return None
    except User.DoesNotExist:
        print(f'User {author_username} does not exist for POST: {title}.')
        return None
    p = Post.objects.create()
    p.title = title
    p.description = description
    p.content = content
    p.viewership = viewership
    p.date_added = date_added
    p.topic = topic
    p.author = author
    p.save()
    return p


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


def create_dummy_categories() -> dict:
    categories_dict = {}

    # def generate_cd(cat_name, cat_parent):
    #     categories_dict[cat_name] = {'name':cat_name,
    #                                  'description':GENERIC_DESC,
    #                                  'date_added':timezone.now(),
    #                                  'parent':cat_parent,
    #                                  }

    def generate_cd(category: dict):
        category['description'] = GENERIC_DESC
        category['date_added'] = timezone.now()
        categories_dict[category['name']] = category

    for category in CategoryDummy.CATEGORIES:
        generate_cd(category)

    return categories_dict


def create_dummy_topics() -> dict:
    topics_dict = {}

    # def generate_td(topic_name, category_name):
    #     topics_dict[topic_name] = { 'name':topic_name,
    #                                 'description':GENERIC_DESC,
    #                                 'date_added':timezone.now(),
    #                                 'category':category_name,
    #                                 }

    def generate_td(topic: dict):
        topic['description'] = GENERIC_DESC
        topic['date_added'] = timezone.now()
        topics_dict[topic['name']] = topic

    for topic in TopicDummy.TOPICS:
        generate_td(topic)

    return topics_dict


# ????
def assign_topics_to_categories(categories_dict: dict, topics_dict: dict):
    for topic in topics_dict:
        category = topics_dict[topic]['categories']
        if not 'topics' in categories_dict[category]:
            categories_dict[category]['topics'] = []
        categories_dict[category]['topics'].append(topics_dict[topic])

    return categories_dict


# def create_dummy_user():
#     for user in UserDummy.USERS:
#         username = user['username']
#         add_user(username=username,
#                  email=user['email'],
#                  password=GENERIC_PASSWORD,
#                  first_name=user['first_name'],
#                  last_name=user['last_name'],
#                  student_id=UserProfileDummy.USER_PROFILES[username]['student_id'],
#                  bio=GENERIC_DESC,
#                  is_admin=False
#                  )
#         print(f'PROFILE add succesful - {username}')

def create_dummy_users_only():
    users_dict = {}

    def generate_ud(user: dict):
        user['password'] = GENERIC_PASSWORD
        users_dict[user['username']] = user

    for user in UserDummy.USERS:
        generate_ud(user)

    return users_dict


def create_dummy_profiles():
    profiles_dict = {}

    def generate_pd(profile: dict):
        profile['bio'] = GENERIC_DESC
        profile['is_admin'] = False
        profiles_dict[profile['username']] = profile

    for profile in UserProfileDummy.USER_PROFILES:
        generate_pd(profile)

    return profiles_dict


def create_dummy_user_profiles():
    user_profiles_dict = {}
    user_profiles_dict = create_dummy_users_only()
    profiles_dict = create_dummy_profiles()

    for profile in profiles_dict.values():
        user = user_profiles_dict[profile['username']]
        for field, value in profile.items():
            if field == 'username':
                continue
            user[field] = value

    return user_profiles_dict


def test_add_category():
    root = Category.__class__
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
                           category_name=category
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


# def populate():
#     cats = create_objects()

#     for cat, cat_data in cats.items():
#         category = add_category(cat, cat_data['description'], cat_data['date_added'], cat_data['parent'])
#     for topic in cat_data['topics']:
#             add_topic(topic['name'], topic['description'], topic['date_added'], category)


#     # Print out the categories we have added.
#     for category in Category.Parent.objects.all():
#         for topic in Topic.objects.filter(category=category):
#             print(f'CATEGORY:TOPIC add succesful - {category}: {topic}')

def dummy_populate():
    categories_dict = create_dummy_categories()
    for cat_data in categories_dict.values():
        added_category = add_category(name=cat_data['name'],
                                      description=cat_data['description'],
                                      date_added=cat_data['date_added'],
                                      parent=cat_data['parent'])
        print(f'CATEGORY add succesful - {added_category.name}')

    topics_dict = create_dummy_topics()
    for top_data in topics_dict.values():
        added_topic = add_topic(name=top_data['name'],
                                description=top_data['description'],
                                date_added=top_data['date_added'],
                                category_name=top_data['category'])
        print(f'TOPIC add succesful - {added_topic.name} IN CATEGORY {added_topic.category}')

    user_profiles_dict = create_dummy_user_profiles()
    for usp_data in user_profiles_dict.values():
        added_profile = add_user(username=usp_data['username'],
                                 email=usp_data['email'],
                                 password=GENERIC_PASSWORD,
                                 first_name=usp_data['first_name'],
                                 last_name=usp_data['last_name'],
                                 student_id=usp_data['student_id'],
                                 bio=usp_data['bio'],
                                 is_admin=usp_data['is_admin'])
        print(f'USER add succesfull - {added_profile.user.username}')


# Start execution here!
if __name__ == '__main__':
    print('Starting Formula1 population script...')
    t_user = test_add_user()
    t_category = test_add_category()
    t_topic = test_add_topic(t_category)
    # dummy_populate()