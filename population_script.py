import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'Formula1.settings')

import django
django.setup()

from django.utils import timezone
from random import randint
from formula.models import *
from db_dummy import *
import json




# ---------------------------------------------------------------
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
    t.save()
    return t

def add_post(title, description, content, viewership, date_added, topic_name, author_username):
    try:
        topic = Topic.objects.get(name=topic_name)
        author = CustomUser.objects.get(username=author_username)
    except Topic.DoesNotExist:
        print(f'Topic {topic_name} does not exist for POST: {title}.')
        return None
    except CustomUser.DoesNotExist:
        print(f'User {author_username} does not exist for POST: {title}.')
        return None
    p = Post.objects.create(topic=topic, author=author, date_added=date_added)
    p.title = title
    p.description = description
    p.content = content
    p.viewership = viewership
    p.date_added = date_added
    p.save()
    return p

def add_custom_user(username, email, password, student_id, bio, is_admin):
    custom_user = CustomUser.objects.get_or_create(username=username, email=email, student_id=student_id)[0]
    custom_user.password = password
    custom_user.student_id = student_id
    custom_user.bio = bio
    custom_user.is_admin = is_admin
    custom_user.save()
    return custom_user

def add_team(name, description):
    tm = Team.objects.get_or_create(name=name)[0]
    tm.description = description
    tm.save()
    return tm

# ----------------------------------------------------------------

def create_dummy_categories() -> dict:
    categories_dict = {}
    
    def generate_cd(category:dict):
        category['description'] = GenericField.DESC
        category['date_added'] = timezone.now()
        categories_dict[category['name']] = category

    for category in CategoryDummy.CATEGORIES:
        generate_cd(category)

    return categories_dict


def create_dummy_topics() -> dict:
    topics_dict = {}

    def generate_td(topic:dict):
        topic['description'] = GenericField.DESC
        topic['date_added'] = timezone.now()
        topics_dict[topic['name']] = topic

    for topic in TopicDummy.TOPICS:
        generate_td(topic)
        
    return topics_dict

def create_dummy_custom_users():
    custom_users_dict = {}

    def generate_cu(custom_users:dict):
        custom_users['password'] = GenericField.PASSWORD
        custom_users['bio'] = GenericField.DESC
        custom_users['is_admin'] = GenericField.IS_ADMIN
        custom_users_dict[custom_users['username']] = custom_users

    for custom_user in CustomUserDummy.CUSTOM_USERS:
        generate_cu(custom_user)

    return custom_users_dict

def create_dummy_post():
    posts_dict = {}
    counter = 0

    def generate_pd(post:dict):
        nonlocal counter
        counter += 1
        post['description'] = GenericField.DESC
        post['content'] = GenericField.CONTENT
        post['viewership'] = randint(0,42)
        post['date_added'] = timezone.now()
        posts_dict[f'post-{counter}'] = post


    for post in PostDummy.POSTS:
        generate_pd(post)

    return posts_dict

def create_dummy_team():
    teams_dict = {}

    def generate_tm(team:dict):
        team['description'] = GenericField.DESC
        teams_dict[team['name']] = team
    
    for team in TeamDummy.TEAMS:
        generate_tm(team)
    
    return teams_dict

# -----------------------------------------------------------

def test_add_category():

    test_category = add_category(name='Test Category',
                 description=GenericField.DESC,
                 date_added=timezone.now(),
                 parent=CategoryDummy.ROOT_PARENT.GENERAL
                 )
    print(f'TEST: CATEGORY add succesful - {test_category.name}')
    return test_category

def test_add_topic(category:Category):
    test_topic = add_topic(name='Fake Topic',
              description=GenericField.DESC,
              date_added=timezone.now(),
              category_name=category
              )
    print(f'TEST: TOPIC add succesful - {test_topic.name} in {category.name}')
    return test_topic

def test_add_post(topic:Topic, author:CustomUser):
    test_post = add_post(title='It\'s a dummy post, Dummy!',
                         description=GenericField.DESC,
                         content=GenericField.CONTENT,
                         viewership=1,
                         date_added=timezone.now(),
                         topic_name=topic.name,
                         author_username=author.username)
    print(f'TEST: POST add succesful - {test_post.title} BY {author.username}')
    return test_post

def test_add_team():
    test_team = add_team(name='Ferrari Test Drive',
                         description=GenericField.DESC)
    print(f'TEST: TEAM add succesful - {test_team.name}')
    return test_team

def test_add_custom_user():
    test_custom_user = add_custom_user(username='fraudilo',
                                       email='fraud@account.com',
                                       password=GenericField.PASSWORD,
                                       student_id='1234567',
                                       bio=GenericField.DESC,
                                       is_admin=GenericField.IS_ADMIN)
    print(f'TEST: CUSTOM USER add succesful - {test_custom_user.username}')
    return test_custom_user
 

# ---------------------------------------------------------

def save_categories(categories_dict:dict):
    for cat_data in categories_dict.values():
        added_category = add_category(name=cat_data['name'], 
                                      description=cat_data['description'], 
                                      date_added=cat_data['date_added'], 
                                      parent=cat_data['parent'])
        print(f'CATEGORY add succesful - {added_category.name}')

def save_topics(topics_dict:dict):
    for top_data in topics_dict.values():
        added_topic = add_topic(name=top_data['name'], 
                                description=top_data['description'], 
                                date_added=top_data['date_added'], 
                                category_name=top_data['category'])
        print(f'TOPIC add succesful - {added_topic.name} IN CATEGORY {added_topic.category}')
 
def save_posts(posts_dict:dict):
    for pos_data in posts_dict.values():
        added_post = add_post(title=pos_data['title'],
                              description=pos_data['description'],
                              content=pos_data['content'],
                              viewership=pos_data['viewership'],
                              date_added=pos_data['date_added'],
                              topic_name=pos_data['topic'],
                              author_username=pos_data['author'])
        print(f'POST add succesful - {added_post.title} BY {added_post.author}')
       
def save_teams(teams_dict:dict):
    for tms_data in teams_dict.values():
        added_team = add_team(name=tms_data['name'],
                              description=tms_data['description'])
        print(f'TEAM add succesful - {added_team.name}')
        
def save_custom_users(custom_users_dict:dict):
    for custom_user in custom_users_dict.values():
        added_custom_user = add_custom_user(username=custom_user['username'],
                                            email=custom_user['email'],
                                            password=custom_user['password'],
                                            student_id=custom_user['student_id'],
                                            bio=custom_user['bio'],
                                            is_admin=custom_user['is_admin'])
        print(f'TEST: CUSTOM USER add succesful - {added_custom_user.username}')

# ----------------------------------------------------------------
def dummy_populate():
    categories_dict = create_dummy_categories()
    save_categories(categories_dict)

    topics_dict = create_dummy_topics()
    save_topics(topics_dict)

    custom_users_dict = create_dummy_custom_users()
    save_custom_users(custom_users_dict)

    posts_dict = create_dummy_post()
    save_posts(posts_dict)

    teams_dict = create_dummy_team()
    save_teams(teams_dict)


# Start execution here! ------------------------------------------
if __name__ == '__main__':
    print('Starting Formula1 population script...')
    t_category = test_add_category()
    t_topic = test_add_topic(t_category)
    t_custom_user = test_add_custom_user()
    t_post = test_add_post(topic=t_topic, author=t_custom_user)
    t_team = test_add_team()
    dummy_populate()
