from django.urls import path
from formula import views
from django.contrib.auth.views import LogoutView
app_name = 'formula'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('profile/<str:username>/', views.show_profile, name='profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('team/<slug:team_slug>/', views.show_team, name='team'),
    path('test/', views.testLogoutView),
    path('register/', views.register, name='register'),
    path('all_users/', views.all_users, name="all_users"),
    path('all_teams/', views.all_teams, name="all_teams"),
    path("teams_and_users/", views.teams_and_users, name="teams_and_users"),
    path('create_post/<slug:category_slug>/<slug:topic_slug>/', views.create_post, name='create_post'),
    path('create_topic/<slug:category_slug>', views.create_topic, name='create_topic'),
    path('<slug:category_slug>/', views.list_topics, name='topics'),
    path('<slug:category_slug>/<slug:topic_slug>/', views.list_posts, name='posts'),
    path('<slug:category_slug>/<slug:topic_slug>/<post_id>/', views.display_post, name='post'),
]
