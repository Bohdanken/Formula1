from population.setup import *
from population.setup import data

def create_dummy_categories() -> dict:
    categories_dict = {}
    
    def generate_cd(category:dict):
        category['description'] = GenericField.DESC
        category['date_added'] = random_datetime()
        categories_dict[category['name']] = category

    for category in CategoryDummy.CATEGORIES:
        generate_cd(category)

    return categories_dict


def create_dummy_topics() -> dict:
    topics_dict = {}

    def generate_td(topic:dict):
        topic['description'] = GenericField.DESC
        topic['date_added'] = random_datetime()
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
        post['viewership'] = randint(1,42)
        post['date_added'] = random_datetime()
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