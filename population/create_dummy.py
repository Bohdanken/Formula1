from population.setup import *
from population.setup import data

def create_dummy_categories() -> dict:
    categories_dict = {}
    
    def generate_cd(category:dict):
        category['description'] = data['GenericField']['desc']
        category['date_added'] = random_datetime()
        categories_dict[category['name']] = category

    for category in data['Category']:
        generate_cd(category)

    return categories_dict


def create_dummy_topics() -> dict:
    topics_dict = {}

    def generate_td(topic:dict):
        topic['description'] = data['GenericField']['desc']
        topic['date_added'] = random_datetime()
        topics_dict[topic['name']] = topic

    for topic in data['Topic']:
        generate_td(topic)
        
    return topics_dict

def create_dummy_custom_users() -> dict:
    custom_users_dict = {}

    def generate_cu(custom_users:dict):
        custom_users['password'] = data['GenericField']['password']
        custom_users['bio'] = data['GenericField']['desc']
        custom_users['is_admin'] = False
        custom_users_dict[custom_users['username']] = custom_users

    for custom_user in data['CustomUser']:
        generate_cu(custom_user)

    return custom_users_dict

def create_dummy_post() -> dict:
    posts_dict = {}
    counter = 0

    def generate_pd(post:dict):
        nonlocal counter
        counter += 1
        post['description'] = data['GenericField']['desc']
        post['content'] = data['GenericField']['content']
        post['viewership'] = randint(1,42)
        post['date_added'] = random_datetime()
        posts_dict[f'post-{counter}'] = post


    for post in data['Post']:
        generate_pd(post)

    return posts_dict

def create_dummy_team() -> dict:
    teams_dict = {}

    def generate_tm(team:dict):
        team['description'] = data['GenericField']['desc']
        teams_dict[team['name']] = team
    
    for team in data['Team']:
        generate_tm(team)
    
    return teams_dict

def assign_dummy_team_member() -> dict:
    team_members_dict = {}

    def generate_mb(team_member:dict):
        team_members_dict[team_member['user']] = team_member

    for team_member in data['TeamMember']:
        generate_mb(team_member)

    return team_members_dict