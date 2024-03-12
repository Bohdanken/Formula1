from django.urls import path
from formula import views

app_name = 'formula'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('<slug:category_slug>/', views.list_topics, name='topics'),
    path('<slug:category_slug>/<slug:topic_slug>/', views.list_posts, name='posts'),
    path('<slug:category_slug>/<slug:topic_slug>/<post_id>/', views.display_post, name='post'),
    path('profile/', views.show_profile, name='profile'),
]