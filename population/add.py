from population.setup import *

def add_category(name, description, date_added, parent):
    c = Category.objects.create(name=name, date_added=date_added)
    c.description = description
    c.parent = parent
    c.save()
    return c

def add_topic(name, description, date_added, category_name):
    cat_slug = __get_slug__(category_name, date_added)
    try:
        category = Category.objects.get(slug=cat_slug)
    except Category.DoesNotExist:
        print(f'Category {category_name} does not exist for TOPIC: {name}.')
        return None
    t = Topic.objects.create(category=category, name=name, date_added=date_added)
    t.description = description
    t.save()
    return t

def add_post(title, description, content, viewership, date_added, topic_name, user_username):
    top_slug = __get_slug__(topic_name, date_added)
    try:
        topic = Topic.objects.get(slug=top_slug)
        user = CustomUser.objects.get(username=user_username)
    except Topic.DoesNotExist:
        print(f'Topic {topic_name} does not exist for POST: {title}.')
        return None
    except CustomUser.DoesNotExist:
        print(f'User {user_username} does not exist for POST: {title}.')
        return None
    p = Post.objects.create(topic=topic, user=user, date_added=date_added)
    p.title = title
    p.description = description
    p.content = content
    p.viewership = viewership
    p.save()
    return p

def add_custom_user(username, email, password, student_id, picture, bio, is_admin):
    cu = CustomUser.objects.create(username=username, email=email, student_id=student_id)
    cu.set_password(password)
    cu.student_id = student_id
    cu.picture = picture
    cu.bio = bio
    cu.is_admin = is_admin
    cu.save()
    return cu

def add_team(name, description):
    tm = Team.objects.create(name=name)
    tm.description = description
    tm.save()
    return tm

def assign_team_member(username, team_name):
    try:
        u = CustomUser.objects.get(username=username)
        tm = Team.objects.get(name=team_name)
    except CustomUser.DoesNotExist:
        print(f'User {username} does not exist for TEAM: {team_name}.')
        return None
    except Team.DoesNotExist:
        print(f'User {username} does not exist for TEAM: {team_name}.')
        return None
    m = TeamMember.objects.create(user=u, team=tm)
    m.save()
    return m

def __get_slug__(name, datetime):
    return slugify(f'{name}-{str(datetime.year)}')