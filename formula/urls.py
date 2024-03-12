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
    # User authentication URLs
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('profile-settings/', views.profile_settings, name='profile_settings'),
    # Admin-specific URLs for category management
    path('admin/categories/', views.admin_categories, name='admin_categories'),
    path('admin/categories/create/', views.create_category, name='create_category'),
    path('admin/categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
]