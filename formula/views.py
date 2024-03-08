from django.shortcuts import render, redirect
from django.http import HttpResponse
from formula.models import Category, Topic
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

def index(request):
    category_list = Category.parent_choices

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    # [depr_code] return render(request, 'rango/index.html', context=context_dict)
    
    # Obtain our Response object early so we can add cookie information.
    response = render(request, 'rango/index.html', context=context_dict)

    # Return response back to the user, updating any cookie changes.
    return response