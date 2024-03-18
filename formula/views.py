from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from formula.models import *
from formula.forms import *
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models.functions import ExtractYear

APP_NAME = 'formula'

def index(request):
    years = list(Category.objects.annotate(year=ExtractYear('date_added')).values_list('year', flat=True))
    years.sort(reverse = True)

    if not request.GET.get("year", default = False):
        year = years[0] if years else datetime.now().year
    else:
        year = int(request.GET.get("year"))
        if year not in years:
            years.append(year)
            years.sort()

    print(year)

    categories = set(Category.objects.annotate(year=ExtractYear('date_added')).filter(year=year))

    context_dict = {
        'years' : years,
        'current_year_categories' : categories
    }

    return render(request, 'formula/index.html', context=context_dict)

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

    ## Dummy data
    if category_slug == "TEST":
        context_dict['category'] = {
            'name' : "TEST",
            'slug' : "TEST",
            'description' : "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        }
        context_dict['topics'] = {
            type("", (object,), {'name' : 'Topic 1', 'slug' : 'TEST'})() : [
                {'title' : "post 1", 'slug' : "TEST"},
                {'title' : "post 2", 'slug' : "TEST"},
                {'title' : "post 3", 'slug' : "TEST"}
            ],
            type("", (object,), {'name' : 'Topic 2', 'slug' : 'TEST'})() : [
                {'title' : "post 4", 'slug' : "TEST"},
            ],
            type("", (object,), {'name' : 'Topic 3', 'slug' : 'TEST'})() : [
                {'title' : "post 5", 'slug' : "TEST"},
                {'title' : "post 6", 'slug' : "TEST"}
            ]
        }

    return render(request, APP_NAME+'/category.html', context=context_dict)


def list_posts(request, category_slug, topic_slug):
    context_dict = {}

    try:
        topic = Topic.objects.get(slug=topic_slug)
        category = topic.category
        context_dict['category'] = category
        context_dict['topic'] = topic
        posts = Post.objects.filter(topic=topic)
        context_dict['posts'] = posts

    except Topic.DoesNotExist:
        context_dict['category'] = None
        context_dict['topic'] = None
        context_dict['posts'] = None

    ## Dummy data
    if topic_slug == "TEST":
        context_dict['topic'] = {
            'name' : "TEST",
            'description' : "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        }
        context_dict['posts'] = [
            {'name' : "post 1"},
            {'name' : "post 2"},
            {'name' : "post 3"},
            {'name' : "post 4"}
        ]

    return render(request, APP_NAME+'/topic.html', context=context_dict)


def display_post(request, category_slug, topic_slug, post_id):
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

    # Dummy data
    if post_id == '0':
        context_dict['post'] = {
            'content' : """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce efficitur vitae nulla sed tincidunt. Quisque justo dui, congue ac dictum id, auctor eget est. Phasellus congue nunc sit amet semper lobortis. Integer dictum ex sed bibendum bibendum. Sed at ullamcorper dui. Etiam id metus et arcu tincidunt mattis ut non ante. Quisque eleifend libero lectus, vitae rutrum turpis bibendum eu. Nulla eros ex, congue sed sem et, dictum mattis nulla. Mauris quis orci sapien. Vestibulum eget varius diam, at scelerisque lorem.

Morbi suscipit, enim sit amet pretium laoreet, risus turpis auctor lectus, et ullamcorper felis massa sed est. Nunc mattis dictum nulla sed volutpat. Vivamus ultricies blandit diam id consectetur. Morbi et orci vel erat suscipit suscipit. Vestibulum pharetra laoreet lectus, lacinia dictum elit suscipit quis. Suspendisse justo enim, pharetra sit amet leo posuere, pulvinar imperdiet lacus. Integer ut sem id turpis interdum volutpat at eu nisi. Donec non nunc venenatis odio semper rhoncus eget a nulla. Mauris aliquam semper iaculis. Donec laoreet mi a ipsum suscipit aliquet. Duis bibendum justo felis, sed maximus enim egestas quis. Vestibulum purus diam, porta id aliquam eu, porttitor vel nibh.

Vivamus ullamcorper, quam eget sodales accumsan, elit justo porta tortor, id placerat diam est nec lacus. Donec tincidunt, sapien non lacinia auctor, risus risus laoreet mauris, rutrum vulputate ipsum dolor non massa. Integer convallis augue vel eros ultrices viverra in in nibh. Nulla at nunc et dolor dictum maximus. Mauris quis fermentum nisi, et sagittis enim. Vestibulum luctus aliquet gravida. Sed convallis orci eu maximus euismod.

Quisque convallis finibus eros. Pellentesque ut auctor magna, in lobortis odio. Nulla at dui tristique, sollicitudin felis et, feugiat tortor. Nam blandit nibh sed quam porta, et suscipit purus porta. Interdum et malesuada fames ac ante ipsum primis in faucibus. Maecenas ultrices venenatis auctor. Aliquam hendrerit lobortis lectus. Suspendisse urna tortor, tempus at hendrerit in, auctor sit amet odio. Pellentesque iaculis erat fringilla ipsum faucibus, nec iaculis felis imperdiet. Aenean diam risus, condimentum a fringilla sit amet, maximus eleifend nunc.

Cras faucibus, nunc scelerisque mattis aliquam, mi augue consequat enim, id commodo neque nisi in elit. Morbi posuere mauris eget erat dignissim, mollis dictum est congue. Curabitur vestibulum semper pellentesque. Aenean eget ipsum vitae quam consequat pellentesque eu et diam. Interdum et malesuada fames ac ante ipsum primis in faucibus. Maecenas ut viverra orci, vitae sollicitudin justo. Nulla commodo iaculis magna, eu ornare leo aliquet consequat. Aliquam sed porttitor arcu, quis dapibus arcu.""",
            'title' : "Lorem ipsum",
            'author' : "Someone",
            'file' : {
                'name' : "Filename.file",
                'url' : "/static/images/logo.png"
            },
            'file_is_image' : True
        }

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
                post.date_added = timezone.now()
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
                topic.date_added = timezone.now()
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
        user = User.objects.get(username=username)
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

def show_team(request, team_slug):
    context_dict = {
        'team' : {
            'name' : "False team",
            'description' : """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus eget neque congue, volutpat ex sed, commodo diam. Aliquam justo libero, porttitor sed luctus ac, vulputate quis mi. Praesent velit metus, vulputate ac eros convallis, luctus elementum justo. Aliquam pulvinar egestas nisi eget porta. Nulla et ligula eget sem pretium volutpat vitae ac justo. Duis imperdiet diam a nisl fermentum, sit amet iaculis ligula ultricies. Suspendisse tincidunt mollis sapien sed accumsan. Phasellus in magna velit. Nam quis blandit nibh, at varius lacus. Sed ut congue enim. Donec libero velit, venenatis id quam sed, tincidunt bibendum purus. Donec eu eros urna. Pellentesque fringilla sem ac imperdiet rhoncus.
Etiam accumsan sollicitudin nisl sed pellentesque. Sed congue pulvinar leo, eu mattis elit volutpat vitae. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam vestibulum turpis vel pretium tempor. Curabitur eros eros, bibendum sit amet elementum non, feugiat a massa. Curabitur ultrices magna maximus sagittis mattis. Morbi convallis massa at lectus ullamcorper, a euismod erat tempus.
Mauris pellentesque tempor erat, vitae lacinia risus. Quisque sed aliquet augue, eget placerat velit. Fusce quis dui et lorem dignissim tincidunt nec vitae diam. Proin sed sem suscipit, semper felis ut, cursus nibh. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Suspendisse viverra mi in libero vehicula scelerisque. Etiam varius turpis massa, eget tempus sapien aliquet id. Proin a sem porttitor, egestas nunc nec, venenatis dolor. Vivamus euismod congue libero nec scelerisque. Nam viverra diam in eleifend fermentum. Interdum et malesuada fames ac ante ipsum primis in faucibus. Phasellus quis nisi at lorem pellentesque gravida. Vivamus sed purus gravida, tristique nulla eu, mattis nibh. Nam erat lorem, lacinia nec pulvinar sed, consectetur nec ligula. Aliquam eleifend magna nec sem semper commodo.
Aenean vitae imperdiet metus, ut efficitur tortor. Sed faucibus varius lorem, aliquam fermentum magna scelerisque vitae. Nam eget enim ipsum. Mauris vehicula hendrerit ligula, eget venenatis lorem sollicitudin eget. Sed placerat nibh sed elit mattis, at mattis nibh tincidunt. Vestibulum eu sagittis tortor. Nulla eu tincidunt tellus. Aliquam maximus est metus, id volutpat risus suscipit semper.
Pellentesque id euismod metus, eget hendrerit felis. Vestibulum et felis in metus semper feugiat ac sit amet mauris. Nulla facilisi. Quisque vitae nisi vitae turpis consequat ultrices. Integer ut felis in nisi faucibus sagittis. Nam erat mauris, posuere non lobortis non, lacinia id nunc. Maecenas tincidunt tellus ut purus blandit, et viverra sapien pretium. Sed elementum sem a ante vehicula semper. Ut a elementum massa. Nullam malesuada augue dignissim nibh facilisis, eu efficitur lacus ullamcorper. Praesent sodales diam ac tortor congue, vel tristique lectus aliquam."""
        },
        'team_lead' : {
            'user' : (team_lead := User.objects.order_by('?')[0]),
        },
        'team_members' : [{'user' : user} for user in User.objects.all().exclude(id=team_lead.id)],
        'topics' : Topic.objects.order_by('?')[:5]
    }
    return render(request, APP_NAME+'/team.html', context=context_dict)
