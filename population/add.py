from population.setup import *

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