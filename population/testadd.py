from population.setup import *
from population.add import *
from django.core.management import call_command

def test_add_category():

    test_category = add_category(name='Test Category',
                 description=GenericField.DESC,
                 date_added=random_datetime(),
                 parent=CategoryDummy.ROOT_PARENT.GENERAL
                 )
    print(f'TEST: CATEGORY add succesful - {test_category.name}')
    return test_category

def test_add_topic(category:Category):
    test_topic = add_topic(name='Fake Topic',
              description=GenericField.DESC,
              date_added=random_datetime(),
              category_name=category
              )
    print(f'TEST: TOPIC add succesful - {test_topic.name} in {category.name}')
    return test_topic

def test_add_post(topic:Topic, author:CustomUser):
    test_post = add_post(title='It\'s a dummy post, Dummy!',
                         description=GenericField.DESC,
                         content=GenericField.CONTENT,
                         viewership=1,
                         date_added=random_datetime(),
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

def run_test(resetafter=True):
    print("----- TEST ------")
    print("Starting test_add.py ...")
    t_category = test_add_category()
    t_topic = test_add_topic(t_category)
    t_custom_user = test_add_custom_user()
    t_post = test_add_post(topic=t_topic, author=t_custom_user)
    t_team = test_add_team()
    # Reset database - emptying the database
    if resetafter:
        call_command('flush', interactive=False)
 