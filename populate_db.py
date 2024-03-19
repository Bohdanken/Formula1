import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'Formula1.settings')

import django
django.setup()

from django.utils import timezone
from random import randint
from formula.models import *
from db_dummy import *

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
        author = User.objects.get(username=author_username)
    except Topic.DoesNotExist:
        print(f'Topic {topic_name} does not exist for POST: {title}.')
        return None
    except User.DoesNotExist:
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

    # def generate_td(topic_name, category_name):
    #     topics_dict[topic_name] = { 'name':topic_name,
    #                                 'description':GENERIC_DESC,
    #                                 'date_added':timezone.now(),
    #                                 'category':category_name,
    #                                 }
    
    def generate_td(topic:dict):
        topic['description'] = GenericField.DESC
        topic['date_added'] = timezone.now()
        topics_dict[topic['name']] = topic

    for topic in TopicDummy.TOPICS:
        generate_td(topic)
        
    return topics_dict

# ????
def assign_topics_to_categories(categories_dict:dict, topics_dict:dict):
    for topic in topics_dict:
        category = topics_dict[topic]['categories']
        if not 'topics' in categories_dict[category]:
            categories_dict[category]['topics'] = []
        categories_dict[category]['topics'].append(topics_dict[topic])
    
    return categories_dict

def __create_dummy_users_only():
    users_dict = {}

    def generate_ud(user:dict):
        user['password'] = GenericField.PASSWORD
        users_dict[user['username']] = user

    for user in UserDummy.USERS:
        generate_ud(user)

    return users_dict

def __create_dummy_profiles():
    profiles_dict = {}

    def generate_up(profile:dict):
        profile['bio'] = GenericField.DESC
        profile['is_admin'] = False
        profiles_dict[profile['username']] = profile
    
    for profile in UserProfileDummy.USER_PROFILES:
        generate_up(profile)
    
    return profiles_dict

def create_dummy_user_profiles():
    user_profiles_dict = {}
    user_profiles_dict = __create_dummy_users_only()
    profiles_dict = __create_dummy_profiles()

    for profile in profiles_dict.values():
        user = user_profiles_dict[profile['username']]
        for field, value in profile.items():
            if field == 'username':
                continue
            user[field] = value

    return user_profiles_dict

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

def test_add_user():
    test_user = add_user(username='normaluser', 
             email='noadmin@privileges.com', 
             password=GenericField.PASSWORD, 
             first_name='Normal', 
             last_name='User', 
             student_id=1111111, 
             bio='This is a generic user with no privileges', 
             is_admin=False
             )
    print(f'TEST: USER add succesful - {test_user.user.username}')
    return test_user

def test_add_post(topic:Topic, author:User):
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
 
def save_user_profiles(user_profiles_dict:dict):
    for usp_data in user_profiles_dict.values():
        added_profile = add_user(username=usp_data['username'],
                                 email=usp_data['email'],
                                 password=GenericField.PASSWORD,
                                 first_name=usp_data['first_name'],
                                 last_name=usp_data['last_name'],
                                 student_id=usp_data['student_id'],
                                 bio=usp_data['bio'],
                                 is_admin=usp_data['is_admin'])
        print(f'USER add succesful - {added_profile.user.username}')

def save_posts(posts_dict:dict):
    for pos_data in posts_dict.values():
        added_post = add_post(title=pos_data['title'],
                              description=pos_data['description'],
                              content=pos_data['content'],
                              viewership=pos_data['viewership'],
                              date_added=pos_data['date_added'],
                              topic_name=pos_data['topic'],
                              author_username=pos_data['author'])
        print(f'POST add succesful - {added_post.title} BY {added_post.author.username}')
       
def save_teams(teams_dict:dict):
    for tms_data in teams_dict.values():
        added_team = add_team(name=tms_data['name'],
                              description=tms_data['description'])
        print(f'TEAM add succesful - {added_team.name}')
        


def dummy_populate():
    categories_dict = create_dummy_categories()
    save_categories(categories_dict)

    topics_dict = create_dummy_topics()
    save_topics(topics_dict)

    user_profiles_dict = create_dummy_user_profiles()
    save_user_profiles(user_profiles_dict)

    posts_dict = create_dummy_post()
    save_posts(posts_dict)

    teams_dict = create_dummy_team()
    save_teams(teams_dict)


# Start execution here!
if __name__ == '__main__':
    print('Starting Formula1 population script...')
    t_user = test_add_user()
    t_category = test_add_category()
    t_topic = test_add_topic(t_category)
    t_post = test_add_post(topic=t_topic, author=t_user.user)
    t_team = test_add_team()
    dummy_populate()