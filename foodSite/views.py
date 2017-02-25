from foodSite.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response,render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from .models import FoodItems, Restaurant
import editdistance

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            stat = form.cleaned_data['choice_field']
            if stat=="Costumer" : status="C"
            else : status="R" 
            user = User.objects.create_user(
            first_name=form.cleaned_data['first_name'],
            last_name=status,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('success/')
    else:
        form = RegistrationForm()
 
    return render(request,
    'registration/register.html',
    {'form': form}
    )
 
def register_success(request):
    return render_to_response(
    'registration/success.html',{'user':request.user}
    )
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
 
@login_required
def home(request):

    menu = FoodItems.objects.all()
    restaurants = Restaurant.objects.all()
    
    #search by category
    
    if request.method == 'GET':
        category_output=[]
        search_query = request.GET.get('search_box', None)
        for item in menu:
            # TODO : replace by edit distance later on
            print item.category, search_query
            a = item.category.lower()
            b = search_query.lower()
            if a == b or a in b or b in a or editdistance.eval(a,b)<=3:
               category_output.append(item)

            print "category"
            for item in category_output:
                print item.name

    return render_to_response(
    'home.html', { 'user': request.user, 'menu' : menu, 'restaurants' : restaurants ,'category_output' : category_output }
    )