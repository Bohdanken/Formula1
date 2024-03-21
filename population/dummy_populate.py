from population.setup import *
from population.add import *
from population.create_dummy import *
from population.save import *

def dummy_populate():
    categories_dict = create_dummy_categories()
    save_categories(categories_dict)

    topics_dict = create_dummy_topics()
    save_topics(topics_dict)

    custom_users_dict = create_dummy_custom_users()
    save_custom_users(custom_users_dict)

    teams_dict = create_dummy_team()
    save_teams(teams_dict)

    team_members_dict = assign_dummy_team_member()
    save_team_members(team_members_dict)

    posts_dict = create_dummy_post()
    save_posts(posts_dict)