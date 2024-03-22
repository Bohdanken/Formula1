from population.setup import *
from population.setup import data
from population.add import *
from django.core.management import call_command
from formula.models import Category

def test_add_category():

    test_category = add_category(name='Test Category',
                 description="Test Category Description",
                 date_added=random_datetime(),
                 parent=Category.GENERAL
                 )
    print(f'TEST: CATEGORY add succesful - {test_category.name}')
    return test_category

def test_add_topic(category:Category):
    test_topic = add_topic(name='Fake Topic',
              description="Fake Topic Description",
              date_added=random_datetime(),
              category_name=category.name
              )
    print(f'TEST: TOPIC add succesful - {test_topic.name} in {category.name}')
    return test_topic

def test_add_post(topic:Topic, user:CustomUser):
    test_post = add_post(title='It\'s a dummy post, Dummy!',
                         description="Post description.",
                         content="Post content.",
                         viewership=1,
                         date_added=random_datetime(),
                         topic_name=topic.name,
                         user_username=user.username)
    print(f'TEST: POST add succesful - {test_post.title} by USER {user.username} in TOPIC {topic.name}')
    return test_post

def test_add_team():
    test_team = add_team(name='Ferrari Test Drive',
                         description="Ferrari Test Drive description")
    print(f'TEST: TEAM add succesful - {test_team.name}')
    return test_team

def test_add_custom_user():
    test_custom_user = add_custom_user(username='fraudilo',
                                       email='fraud@account.com',
                                       password="boohoopassword",
                                       student_id='2000001',
                                       picture='static\images\Default_pfp.svg',
                                       bio="fraudilo's bio",
                                       is_admin=False)
    print(f'TEST: CUSTOM USER add succesful - {test_custom_user.username}')
    return test_custom_user

def  test_assign_team_member(user:CustomUser, team:Team):
    test_team_member = assign_team_member(username=user.username,
                                          team_name=team.name)
    print(f'TEST: TEAM MEMBER assign succesful - {test_team_member.user.username} to TEAM {test_team_member.team.name}')
    return test_team_member

def test_assign_team_lead(user:CustomUser, team:Team, topic_list):
    test_team_lead = assign_team_lead(username=user.username,
                                      team_name=team.name,
                                      topic_list=topic_list)
    print(f'TEST: TEAM LEAD assign succesful - {test_team_lead.user.username} to TEAM {test_team_lead.team.name}')
    return test_team_lead


# ------ RUN TEST --------
def run_test(resetafter=True):
    print("------------------ TEST -------------------------------------------------------------")
    print("Starting test_add.py ...")

    t_category = test_add_category()
    t_topic = test_add_topic(t_category)
    t_custom_user = test_add_custom_user()
    t_post = test_add_post(topic=t_topic, user=t_custom_user)
    t_team = test_add_team()
    t_team_member = test_assign_team_member(t_custom_user, t_team)
    t_team_lead = test_assign_team_lead(t_custom_user, t_team, [t_topic])
    
    print("----------------- TEST SUCCESS ------------------------------------------------------")
    print()

    print("Flushing database - emptying the database for actual population.")
    if resetafter:
        call_command('flush', interactive=False)
 