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
    text_description = "A forum dedicated to allowing users to communicate and learn about the development, upkeep and use of race cars"
    contact_email = "2345678@student.gla.ac.uk"

    context_dict = {}
    context_dict['text'] = text_description
    context_dict['contact'] = contact_email

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
            'user' : (team_lead := CustomUser.objects.order_by('?')[0]),
        },
        'team_members' : [{'user' : user} for user in CustomUser.objects.all().exclude(email=team_lead.email)],
        'topics' : Topic.objects.order_by('?')[:5]
    }
    return render(request, APP_NAME+'/team.html', context=context_dict)
