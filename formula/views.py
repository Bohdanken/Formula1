from datetime import datetime
from zipfile import ZipFile
import random

from django.conf.global_settings import LOGIN_URL
from django.contrib.auth.views import LogoutView
from django.conf.global_settings import LOGIN_URL
from django.shortcuts import render, redirect
from django.http import  HttpResponseForbidden
from django.http import HttpResponse, FileResponse
from formula.forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.db.models.functions import ExtractYear
from django.urls import reverse, NoReverseMatch
from django.shortcuts import get_object_or_404
from .forms import CustomUserChangeForm

from zipfile import ZipFile
from io import BytesIO


from Formula1.settings import MEDIA_ROOT

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
        'year' : year,
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
        context_dict['topics'] = { topic : Post.objects.filter(topic = topic) for topic in topics } #[{'post' : post, 'pfp' : post.author.picture} for post in list(sorted(Post.objects.filter(topic=topic), key = lambda post : post.viewership))[:3]] for topic in topics }
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
            topic : posts
        }

        return render(request, APP_NAME+'/topic.html', context=context_dict)

    except Topic.DoesNotExist:
        return render(request, APP_NAME+'/topic.html', context={}, status=404)


def display_post(request, category_slug, topic_slug, post_id):
    if request.GET.get('file', default=False):
        if Post.objects.get(id=post_id).file:
            zip_path = Post.objects.get(id=post_id).file.path
            zipfile = ZipFile(zip_path, 'r')
            file_bytes = zipfile.read(request.GET.get('file'))
            return FileResponse(BytesIO(file_bytes), as_attachment=True, filename=request.GET.get('file'))
    context_dict = {}
    try:
        post = Post.objects.get(id=post_id)
        context_dict['post'] = post
        context_dict['topic'] = post.topic
        context_dict['category'] = post.topic.category
        context_dict['images'] = []
        context_dict['files'] = []

        if post.file:
            zipfile = ZipFile(post.file.path, 'r')
            for filename in zipfile.namelist():
                if filename.split('.')[-1].lower() in {'apng', 'cur', 'gif', 'ico', 'jfif', 'jpeg', 'jpg', 'pjp', 'pjpeg', 'png', 'svg'}:
                    context_dict['images'].append(filename)
                else:
                    context_dict['files'].append(filename)

        return render(request, APP_NAME+'/post.html', context=context_dict)
    
    except Post.DoesNotExist:
        return render(request, APP_NAME+'/404.html', context={}, status=404)


def query_result(request, title_query):
    context_dict = {}

    posts = Post.objects.filter(title__contains=title_query)
    context_dict['posts'] = posts
    return render(request, APP_NAME + '/post.html', context=context_dict)


@login_required(login_url=LOGIN_URL)
def create_post(request, category_slug, topic_slug):
    try:
        topic = Topic.objects.get(slug=topic_slug)
    except Topic.DoesNotExist:
        return redirect(APP_NAME + ':index')

    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            if topic:
                post = form.save(commit=False)
                post.topic = topic
                post.user = CustomUser.objects.get(username=request.user.get_name())
                post.date_added = timezone.now()

                if 'file' in request.FILES:

                    # Should allow for 99,636,535,482,328,266,092,631,578,144,895,845,295,049,065,188,420,485,120
                    # unique filenames (or 99 septendecillion 636 sexdecillion 535 quindecillion 482 quattuordecillion
                    # 328 tredecillion 266 duodecillion 92 undecillion 631 decillion 578 nonillion 144 octillion
                    # 895 septillion 845 sextillion 295 quintillion 49 quadrillion 65 trillion 188 billion
                    # 420 million 485 thousand one hundred and twenty)

                    filename_chars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_-0123456789"

                    while True:
                        filename = "".join(random.choice(filename_chars) for i in range(random.randint(16, 32))) + ".zip"
                        try:
                            zipfile = ZipFile(MEDIA_ROOT+"\\post_files\\" + filename, mode='x')
                        except FileExistsError: continue
                        else: break

                    for file in request.FILES.getlist('file'):
                        zipfile.writestr(file.name, file.read())

                    post.file.name = "post_files\\" + filename
                    zipfile.close()
                post.save()

                return redirect(reverse(APP_NAME + ':post',
                                        kwargs={'category_slug': category_slug, 'topic_slug': topic_slug, 'post_id' : post.id}))

        else:
            print(form.errors)

    context_dict = {'form': form, 'topic': topic, 'category': topic.category }
    return render(request, APP_NAME + '/create-post.html', context=context_dict)


@login_required(login_url=LOGIN_URL)
def create_topic(request, category_slug):
    try:
        category = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        category = None
    if category is None:
        return redirect(APP_NAME + ':index')
    if not request.user.is_superuser:
        try:
            team_lead = TeamLead.objects.get(user=request.user)
            if not team_lead.topic_access.filter(category=category).exists():
                return HttpResponseForbidden("You do not have access to this category.")
        except TeamLead.DoesNotExist:
            return HttpResponseForbidden("Access denied.")
    form = TopicForm()
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            if category:
                topic = form.save(commit=False)
                topic.category = category
                topic.date_added = timezone.now()
                topic.save()

                return redirect(reverse(APP_NAME + ':posts',
                                        kwargs={'category_slug': category_slug, 'topic_slug' : topic.slug}))
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, APP_NAME + '/create-topic.html', context=context_dict)


@login_required(login_url=LOGIN_URL)
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
    context_dict = {}
    user = get_object_or_404(CustomUser, username=username)
    context_dict['user'] = user
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('formula:profile', username=request.user.username)
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'registration/edit_profile.html', context=context_dict)


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

def redirectView(request):
    return redirect("formula/")

class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # User is not authenticated, redirect to login page or any other page
            return redirect('login')  # Assuming you have a URL named 'login'
        # User is authenticated, proceed with the normal LogoutView flow
        return super().dispatch(request, *args, **kwargs)


def show_team(request, team_slug):
    context_dict = {}
    try:
        context_dict['team'] = Team.objects.get(slug=team_slug)
        context_dict['team_members'] = TeamMember.objects.filter(team=context_dict['team'])
        context_dict['team_lead'] = TeamLead.objects.filter(team=context_dict['team']).first()
        context_dict['team_members_names'] = [context_dict['team_lead'].user.username] + [memebr.user.username for memebr in context_dict['team_members']]
        context_dict['view_topic_page'] = True
        context_dict['topics'] = {
            topic : list(sorted(Post.objects.filter(topic=topic), key = lambda post : post.viewership))[:3] for topic in context_dict['team_lead'].topic_access.all() #[{'post' : post, 'pfp' : UserProfile.objects.get(user = post.author).picture} for post in list(sorted(Post.objects.filter(topic=topic), key = lambda post : post.viewership))[:3]] for topic in context_dict['team_lead'].topic_access.all()
        }
        context_dict['selected'] = context_dict['team_lead'].user
        if request.GET.get("profile", default=False) in context_dict['team_members_names']:
            context_dict['selected'] = CustomUser.objects.get(username=request.GET.get('profile'))
        return render(request, APP_NAME+'/team.html', context=context_dict)
    except Team.DoesNotExist:
        return render(request, APP_NAME+'/404.html', context=context_dict, status=404)


