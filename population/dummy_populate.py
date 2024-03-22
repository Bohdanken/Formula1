from population.setup import *
from population.add import *
from population.create_dummy import *
from population.save import *
from formula.models import Clone, Category, Topic, Post

def dummy_populate():
    custom_users_dict = create_dummy_custom_users()
    save_custom_users(custom_users_dict)
    
    categories_dict = create_dummy_categories()
    save_categories(categories_dict)

    topics_dict = create_dummy_topics()
    save_topics(topics_dict)

    teams_dict = create_dummy_team()
    save_teams(teams_dict)

    team_members_dict = assign_dummy_team_member()
    save_team_members(team_members_dict)

    team_leads_dict = assign_dummy_team_lead()
    save_team_leads(team_leads_dict)

    posts_dict = create_dummy_post()
    save_posts(posts_dict)

    Clone.clone_all(Category, CLONE)
    Clone.clone_all(Topic, CLONE)
    Clone.clone_all(Post, CLONE)