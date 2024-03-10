from django.shortcuts import render, redirect
from django.http import HttpResponse
from formula.models import Category, Topic
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models.functions import ExtractYear
from urls import app_name

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

    response = render(request, app_name+'/index.html', context=context_dict)

    # Return response back to the user, updating any cookie changes.
    return response


def about(request):
    text_description = "A forum dedicated to allowing users to communicate and learn about the development, upkeep and use of race cars"
    contact_email = "2345678@student.gla.ac.uk"

    context_dict = {}
    context_dict['text'] = text_description
    context_dict['contact'] = contact_email

    return render(request, app_name+'/about.html', context=context_dict)



def show_topics(request, category_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_slug)
        topics = Topic.objects.filter(category=category)
        context_dict['topics'] = topics
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['topics'] = None
        context_dict['category'] = None

    return render(request, app_name+'/category.html', context=context_dict)


def show_posts(request,)