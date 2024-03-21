from datetime import datetime

from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from formula.forms import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models.functions import ExtractYear
from django.urls import reverse, NoReverseMatch
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import get_object_or_404
from .forms import CustomUserChangeForm


APP_NAME = 'formula'
REGISTER_NAME = 'registration'


def index(request):
    years = list(set(Category.objects.annotate(year=ExtractYear('date_added')).values_list('year', flat=True)))
    years.sort(reverse = True)

    if not request.GET.get("year", default=False):
        year = years[0] if years else datetime.now().year
    else:
        year = int(request.GET.get("year"))
        if year not in years:
            years.append(year)
            years.sort()

    categories = set(Category.objects.annotate(year=ExtractYear('date_added')).filter(year=year))

    context_dict = {
        'years': years,
        'current_year_categories': categories
    }

    return render(request, 'formula/index.html', context=context_dict)


def about(request):

    context_dict = {
        'text_description' : "A forum dedicated to allowing users to communicate and learn about the development, upkeep and use of race cars. For Racers, by Racers.",
        'contact_email' : "formulau1@outlook.com"
    }

    return render(request, APP_NAME + '/about.html', context=context_dict)


def list_topics(request, category_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_slug)
        topics = Topic.objects.filter(category=category)
        context_dict['category'] = category
        context_dict['topics'] = { topic : [{'post' : post, 'pfp' : UserProfile.objects.get(user = post.author).picture} for post in list(sorted(Post.objects.filter(topic=topic), key = lambda post : post.viewership))[:3]] for topic in topics }
        return render(request, APP_NAME+'/category.html', context=context_dict)

    except Category.DoesNotExist:
        return render(request, APP_NAME+'/category.html', context={}, status=404)


def list_posts(request, category_slug, topic_slug):
    context_dict = {}

    try:
        topic = Topic.objects.get(slug=topic_slug)
        category = topic.category
        context_dict['category'] = category
        context_dict['topic'] = topic
        posts = Post.objects.filter(topic=topic)
        context_dict['topics'] = {
            topic : [{'post' : post, 'pfp' : UserProfile.objects.get(user = post.author).picture} for post in posts]
        }

        return render(request, APP_NAME+'/topic.html', context=context_dict)

    except Topic.DoesNotExist:
        return render(request, APP_NAME+'/topic.html', context={}, status=404)


def display_post(request, category_slug, topic_slug, post_id):
    context_dict = {}
    try:
        post = Post.objects.get(id=post_id)
        context_dict['post'] = post
        context_dict['topic'] = post.topic
        context_dict['category'] = post.topic.category
        context_dict['file_is_image'] = post.file.name.split('.')[-1].lower() in {'apng', 'cur', 'gif', 'ico', 'jfif', 'jpeg', 'jpg', 'pjp', 'pjpeg', 'png', 'svg'}
        
        return render(request, APP_NAME+'/post.html', context=context_dict)
    
    except Post.DoesNotExist:
        return render(request, APP_NAME+'/post.html', context={}, status=404)


def query_result(request, title_query):
    context_dict = {}

    posts = Post.objects.filter(title__contains=title_query)
    context_dict['posts'] = posts
    return render(request, APP_NAME + '/post.html', context=context_dict)


@login_required
def create_post(request, topic_slug):
    try:
        topic = Topic.objects.get(slug=topic_slug)
    except Topic.DoesNotExist:
        topic = None

    # You cannot ade a post to a Topic that does not exist
    if topic is None:
        return redirect(APP_NAME + ':index')

    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            if topic:
                post = form.save(commit=False)
                post.topic = topic
                post.author = CustomUser.objects.get(user=request.user)
                post.date_added = timezone.now()
                if 'file' in request.FILES:
                    post.file = request.FILES['file']
                post.save()

                return redirect(reverse(APP_NAME + ':display_post',
                                        kwargs={'topic_slug': topic_slug}))

        else:
            print(form.errors)

    context_dict = {'form': form, 'topic': topic}
    return render(request, APP_NAME + '/add_post.html', context=context_dict)


@login_required
def create_topic(request, category_slug):
    try:
        category = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        category = None

    # You cannot ade a post to a Topic that does not exist
    if category is None:
        return redirect(APP_NAME + ':index')

    form = TopicForm()

    if request.method == 'POST':
        form = TopicForm(request.POST)

        if form.is_valid():
            if category:
                topic = form.save(commit=False)
                topic.category = category
                topic.date_added = timezone.now()
                topic.save()

                return redirect(reverse(APP_NAME + ':show_topics',
                                        kwargs={'category_slug': category_slug}))

        else:
            print(form.errors)

    context_dict = {'form': form, 'topic': category}
    return render(request, APP_NAME + '/add_post.html', context=context_dict)


@login_required
def show_profile(request, username):
    context_dict = {}

    try:
        user = CustomUser.objects.get(username=username)
        context_dict['user'] = user
    except CustomUser.DoesNotExist:
        context_dict['user'] = None

    return render(request, APP_NAME + '/profile.html', context=context_dict)

@login_required
def edit_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('formula:profile', username=request.user.username)
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'registration/edit_profile.html')


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            if 'picture' in request.FILES:
                user.picture = request.FILES['picture']

            user.save()
            registered = True

        else:
            print(user_form.errors, user_form.errors)

    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render(request, REGISTER_NAME + '/register.html', context={'user_form': user_form,
                                                                      'registered': registered})


def testLogoutView(request):
    return render(request, REGISTER_NAME + '/logout.html', context={})


class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # User is not authenticated, redirect to login page or any other page
            return redirect('login')  # Assuming you have a URL named 'login'
        # User is authenticated, proceed with the normal LogoutView flow
        return super().dispatch(request, *args, **kwargs)

def show_team(request, team_slug):
    try:
        context_dict={}
        context_dict['team'] = Team.objects.get(slug=team_slug)
        context_dict['team_members'] = TeamMember.objects.filter(team=context_dict['team'])
        context_dict['team_lead'] = TeamLead.objects.get(team=context_dict['team'])
        context_dict['team_members_names'] = [context_dict['team_lead'].user.username] + [memebr.user.username for memebr in context_dict['team_members']]
        context_dict['view_topic_page'] = True
        context_dict['topics'] = {
            topic : [{'post' : post, 'pfp' : UserProfile.objects.get(user = post.author).picture} for post in list(sorted(Post.objects.filter(topic=topic), key = lambda post : post.viewership))[:3]] for topic in context_dict['team_lead'].topic_access.all()
        }
        context_dict['selected'] = context_dict['team_lead'].user

        if request.GET.get("profile", default=False) in context_dict['team_members_names']:
            context_dict['selected'] = CustomUser.objects.get(username=request.GET.get('profile'))

        return render(request, APP_NAME+'/team.html', context=context_dict)

    except Team.DoesNotExist:
        return render(request, APP_NAME+'/404.html', context=context_dict, status=404)
