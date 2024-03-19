import os
import django
from django.db import IntegrityError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Formula1.settings')
django.setup()

from formula.models import Category, Topic, CustomUser
from django.utils import timezone

# Given dummy data classes
class CategoryDummy:
    CATEGORIES = [
        ('Engineering Project', Category.EVEHICLE),
        ('Design', Category.GENERAL),
        ('Software Development', Category.EVEHICLE),
        ('Business Operations', Category.OPERATION),
        ('Research and Development', Category.EVEHICLE),
        ('Testing', Category.EVEHICLE),
        ('Marketing', Category.OPERATION),
        ('Finance', Category.OPERATION),
        ('Events', Category.OPERATION),
        ('Education', Category.GENERAL),
        ('Community Outreach', Category.OPERATION),
    ]

class TopicDummy:
    TOPICS = [
        ('Vehicle Design', 'Design'),
        ('Graphic Design', 'Design'),
        ('Aerodynamics', 'Engineering Project'),
        ('Chassis Design', 'Engineering Project'),
        ('Powertrain', 'Engineering Project'),
        ('Suspension', 'Engineering Project'),
        ('Electronics', 'Engineering Project'),
        ('Materials', 'Engineering Project'),
        ('Testing and Simulation', 'Engineering Project'),
        ('Sponsorship', 'Business Operations'),
        ('Event Management', 'Business Operations'),
        ('Market Research', 'Research and Development'),
        ('Product Development', 'Research and Development'),
        ('Financial Planning', 'Finance'),
        ('Budgeting', 'Finance'),
        ('Advertising', 'Marketing'),
        ('Public Relations', 'Marketing'),
        ('Software Engineering', 'Software Development'),
        ('Data Analysis', 'Software Development'),
        ('Community Outreach', 'Community Outreach'),
        ('Educational Programs', 'Education'),
        ('Volunteer Management', 'Education'),
        ('Sales', 'Business Operations'),
        ('Customer Service', 'Business Operations'),
        ('Project Management', 'Business Operations'),
    ]

class UserDummy:
    USERS = [
        {
            'username': 'jeffreymulloc',
            'email': 'jeffr4y@gmail.com',
            'first_name': 'Jeffrey',
            'student_id': 2348783,

            'last_name': 'Mulloc',
        },
        {
            'username': 'bobbykeren',
            'email': 'bob@ed.uk',
            'first_name': 'Bob',
            'student_id': 2348782,

            'last_name': 'Keren',
        },
        {
            'username': 'alicewond',
            'email': 'alice@gmail.com',
            'first_name': 'Alice',
            'student_id': 2348784,

            'last_name': 'Wond',
        },
        {
            'username': 'dannyboy',
            'email': 'danny@web.com',
            'first_name': 'Danny',
            'student_id': 2348781,

            'last_name': 'Boy',
        },
        {
            'username': 'sarahjane',
            'email': 'sarah@gmail.com',
            'first_name': 'Sarah',
            'student_id': 2348785,

            'last_name': 'Jane',
        },
        {
            'username': 'michaelscott',
            'email': 'michael@dundermifflin.com',
            'first_name': 'Michael',
            'student_id': 2348786,

            'last_name': 'Scott',
        },
        # New users added below
        {
            'username': 'pambeesly',
            'email': 'pam@dundermifflin.com',
            'first_name': 'Pam',
            'student_id': 2348787,
            'last_name': 'Beesly',
        },
        {
            'username': 'jimhalpert',
            'email': 'jim@dundermifflin.com',
            'first_name': 'Jim',
            'student_id': 2348792,

            'last_name': 'Halpert',
        },
        {
            'username': 'dwightschrute',
            'email': 'dwight@dundermifflin.com',
            'first_name': 'Dwight',
            'student_id': 2348796,

            'last_name': 'Schrute',
        },
    ]


# Functions to add objects to the database
def add_category(name, type):
    c, created = Category.objects.get_or_create(name=name, defaults={'parent': type, 'date_added': timezone.now()})
    print(f"Category '{c.name}' added.")
    return c

def add_topic(name, category_name):
    category = Category.objects.get(name=category_name)
    t, created = Topic.objects.get_or_create(name=name, defaults={'category': category, 'date_added': timezone.now()})
    print(f"Topic '{t.name}' added.")
    return t

def add_user(email, username, student_id, first_name, last_name):
    try:
        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={'username': username, 'first_name': first_name, 'last_name': last_name, 'student_id': student_id}
        )
        if created:
            user.set_password("sa")
            user.bio="sa"
            user.is_admin=False
            user.save()
            print(f"User '{user.username}' added successfully.")
        else:
            print(f"User '{user.username}' already exists.")
    except IntegrityError as e:
        print(f"Error adding user '{username}': {e}. It's possible the student ID is already in use.")

# Main function to populate the database
def populate():
    for cat_name, cat_type in CategoryDummy.CATEGORIES:
        add_category(cat_name, cat_type)

    for topic_name, cat_name in TopicDummy.TOPICS:
        add_topic(topic_name, cat_name)

    for user in UserDummy.USERS:
        add_user(**user)

# Entry point
if __name__ == '__main__':

    print("Starting population script...")
    populate()
    print("Database populated successfully!")
