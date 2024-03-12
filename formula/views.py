from django.shortcuts import render, redirect
from django.http import HttpResponse
from formula.models import Category, Topic, Post, UserProfile
from formula.forms import TopicForm, PostForm, UserForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models.functions import ExtractYear

APP_NAME = 'formula'

def index(request):
    """
    EXPECTED DATA STRUCTURE
    -------------------------
    cat_list = {
        2022: [cat1, cat2, cat3],
        2023: [cat4, cat5, cat6],
        2024: [cat7, cat8, cat9],
    }

    ACCESS LIKE THIS
    -------------------
    cat_list[2022] -> [cat1, cat2, cat3]
    
    """

    parent_list = Category.Parent.CHOICESET
    
    # get a set of year
    year_set = set(Category.objects.all().annotate(year=ExtractYear('date_added')).values_list('year', flat=True))
    
    category_by_year_dict = {year:Category.objects.filter(date_added_exact=year) for year in year_set}

    context_dict = {}
    context_dict['parents'] = parent_list
    context_dict['year_list'] = year_set
    context_dict['category_by_year'] = category_by_year_dict

    response = render(request, APP_NAME+'/index.html', context=context_dict)

    # Return response back to the user, updating any cookie changes.
    return response


def about(request):
    text_description = "A forum dedicated to allowing users to communicate and learn about the development, upkeep and use of race cars"
    contact_email = "2345678@student.gla.ac.uk"

    context_dict = {}
    context_dict['text'] = text_description
    context_dict['contact'] = contact_email

    return render(request, APP_NAME+'/about.html', context=context_dict)



def list_topics(request, category_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_slug)
        topics = Topic.objects.filter(category=category)
        context_dict['topics'] = topics
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['topics'] = None
        context_dict['category'] = None

    return render(request, APP_NAME+'/category.html', context=context_dict)


def list_posts(request, topic_slug):
    context_dict = {}

    try:
        topic = Topic.objects.get(topic=topic_slug)
        category = topic.category
        context_dict['category'] = category
        context_dict['topic'] = topic
        posts = Post.objects.filter(topic=topic)
        context_dict['posts'] = posts

    except Topic.DoesNotExist:
        context_dict['category'] = None
        context_dict['topic'] = None
        context_dict['posts'] = None

    return render(request, APP_NAME+'/posts.html', context=context_dict)


def display_post(request, post_id):
    context_dict = {}
    try:
        post = Post.objects.get(id=post_id)
        context_dict['post'] = post
        context_dict['topic'] = post.topic
        context_dict['category'] = post.topic.category
    
    except Post.DoesNotExist:
        context_dict['post'] = None
        context_dict['topic'] = None
        context_dict['category'] = None

    return render(request, APP_NAME+'/post.html', context=context_dict)


def query_result(request, title_query):
    context_dict = {}

    posts = Post.objects.filter(title__contains=title_query)
    context_dict['posts'] = posts
    return render(request, APP_NAME+'/post.html', context=context_dict)


@login_required
def create_post(request, topic_slug):

    try:
        topic = Topic.objects.get(slug=topic_slug)
    except Topic.DoesNotExist:
        topic = None

    # You cannot ade a post to a Topic that does not exist
    if topic is None:
        return redirect(APP_NAME+':index')

    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            if topic:
                post = form.save(commit=False)
                post.topic = topic
                post.author = UserProfile.objects.get(user=request.user)
                post.date_added = datetime.now()
                if 'file' in request.FILES:
                    post.file = request.FILES['file']
                post.save()

                return redirect(reverse(APP_NAME+':display_post', 
                                        kwargs={'topic_slug':topic_slug}))
            
        else:
            print(form.errors)
    
    context_dict = {'form':form, 'topic':topic}
    return render(request, APP_NAME+'/add_post.html', context=context_dict)


@login_required
def create_topic(request, category_slug):

    try:
        category = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        category = None

    # You cannot ade a post to a Topic that does not exist
    if category is None:
        return redirect(APP_NAME+':index')

    form = TopicForm()

    if request.method == 'POST':
        form = TopicForm(request.POST)

        if form.is_valid():
            if category:
                topic = form.save(commit=False)
                topic.category = category
                topic.date_added = datetime.now()
                topic.save()

                return redirect(reverse(APP_NAME+':show_topics', 
                                        kwargs={'category_slug':category_slug}))
            
        else:
            print(form.errors)
    
    context_dict = {'form':form, 'topic':category}
    return render(request, APP_NAME+'/add_post.html', context=context_dict)


def show_profile(request, username):
    context_dict = {}

    try:
        user = UserProfile.objects.get(username=username)
        context_dict['user'] = user
    except UserProfile.DoesNotExist:
        context_dict['user'] = None

    return render(request, APP_NAME+'/profile.html', context=context_dict)


def register(request):
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        
        else:
            print(user_form.errors, profile_form.errors)
    
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request, APP_NAME+'/register.html', context={'user_form': user_form,
                                                           'profile_form': profile_form,
                                                           'registered': registered })


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:

            if user.is_active:
                login(request, user)
                return redirect(reverse(APP_NAME+':index'))
            else:
                return HttpResponse(f"Your {APP_NAME.capitalize} account is disabled.")
        
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied")
        
    else:
        return render(request, APP_NAME+'/login.html')