from population.setup import *
from population.add import *

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
 
def save_posts(posts_dict:dict):
    for pos_data in posts_dict.values():
        added_post = add_post(title=pos_data['title'],
                              description=pos_data['description'],
                              content=pos_data['content'],
                              viewership=pos_data['viewership'],
                              date_added=pos_data['date_added'],
                              topic_name=pos_data['topic'],
                              user_username=pos_data['user'])
        print(f'POST add succesful - {added_post.title} by USER {added_post.user.username}')
       
def save_teams(teams_dict:dict):
    for tms_data in teams_dict.values():
        added_team = add_team(name=tms_data['name'],
                              description=tms_data['description'])
        print(f'TEAM add succesful - {added_team.name}')
        
def save_custom_users(custom_users_dict:dict):
    for custom_user in custom_users_dict.values():
        added_custom_user = add_custom_user(username=custom_user['username'],
                                            email=custom_user['email'],
                                            password=custom_user['password'],
                                            student_id=custom_user['student_id'],
                                            picture=custom_user['picture'],
                                            bio=custom_user['bio'],
                                            is_admin=custom_user['is_admin'])
        print(f'USER add succesful - {added_custom_user.username}')

def save_team_members(team_members_dict:dict):
    for team_member in team_members_dict.values():
        assigned_team_member = assign_team_member(username=team_member['user'],
                                               team_name=team_member['team'])
        print(f'TEAM MEMBER add succesful - USER {assigned_team_member.user.username} to TEAM {assigned_team_member.team.name}')

def save_team_leads(team_leads_dict:dict):
    for team_lead in team_leads_dict.values():
        assigned_team_lead = assign_team_lead(username=team_lead['user'],
                                              team_name=team_lead['team'],
                                              topic_list=team_lead['topic_access'])
        print(f'TEAM LEAD add succesful - USER {assigned_team_lead.user.username} to TEAM {assigned_team_lead.team.name}')
     