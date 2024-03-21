from django.urls import path
from formula import views
from django.contrib.auth.views import LogoutView
app_name = 'formula'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    #path('profile/', views.show_profile, name='profile'),
    path('profile/<str:username>/', views.show_profile, name='profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('team/<slug:team_slug>/', views.show_team, name='team'),
    path('test/', views.testLogoutView),
    #path('search/', views.search_results, name='search'),
    #path('search/?query=<str:search_query>', views.search_query, name='search_query'),

    # User authentication URLs
    #path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('create_post/', views.create_post, name='create_post'),
    path('create_topic/', views.create_topic, name='create_topic'),
    #path('logout/', views.user_logout, name='logout'),
    #path('edit-profile/', views.edit_profile, name='edit_profile'),
    #path('profile-settings/', views.profile_settings, name='profile_settings'),
    
    # Admin-specific URLs for category management
    #path('admin/categories/', views.admin_categories, name='admin_categories'),
    #path('admin/categories/create/', views.create_category, name='create_category'),
    #path('admin/categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),

    path('<slug:category_slug>/', views.list_topics, name='topics'),
    path('<slug:category_slug>/<slug:topic_slug>/', views.list_posts, name='posts'),
    path('<slug:category_slug>/<slug:topic_slug>/<post_id>/', views.display_post, name='post'),
]
