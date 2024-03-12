from django.urls import path
from formula import views

app_name = 'formula_forum'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('<slug:category_slug>/', views.list_topics, name='show_topics'),
    path('<slug:category_slug>/create_topic/', views.create_topic, name='create_topic'),
    path('<slug:category_slug>/<slug:topic_slug>/', views.list_posts, name='show_posts'),
    path('<slug:category_slug>/<slug:topic_slug>/post/<post_id>/', views.display_post, name='display_post'),
    path('<slug:category_slug>/<slug:topic_slug>/create_post/', views.create_post, name='create_post'),
    path('profile/', views.show_profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
]