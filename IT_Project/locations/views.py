import sqlite3
from django.contrib import messages
from django.views.generic.edit import CreateView

from . import models
from .models import Location, Order, locations_order, locations_customuser_id
from django.shortcuts import render, redirect, HttpResponse


from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

# Create your views here.

# class LocationView(CreateView):

#     model = Location
#     fields = ['address']
#     template_name = 'locations/home.html'
#     success_url = '/'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['locations'] = Location.objects.all()
#         context['mapbox_access_token'] = 'pk.eyJ1IjoiYWxlc3NpbzIxIiwiYSI6ImNsZWszb2twMzBoa3QzcHBnNnhqbHIwMHUifQ.AW2-2b4IYh4qqPqqzMXy8Q'
        
#         return context

def index(request):
    context = {}
    context['mapbox_access_token'] = 'pk.eyJ1IjoiYWxlc3NpbzIxIiwiYSI6ImNsZWszb2twMzBoa3QzcHBnNnhqbHIwMHUifQ.AW2-2b4IYh4qqPqqzMXy8Q'
    context['locations'] = Location.objects.all()
    locations_with_bike = Location.objects.filter(vehicle__type__name='Bike').distinct()
    context['locations_bike'] = locations_with_bike
    response = render(request, 'locations/home.html', context=context)
    return response



def register(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname").strip()
        lastname = request.POST.get("lastname").strip()
        username = request.POST.get("username").strip()
        passwd = request.POST.get("passwd").strip()
        email =  request.POST.get("email").strip()

        with sqlite3.connect("./db.sqlite3") as db:
            cursor = db.cursor()
            cursor.execute(
            """SELECT username
                    From locations_customuser
                    WHERE username= '{}' """.format(username)
        )
        res = cursor.fetchone()
        if res:
            db.close()
            messages.error(request, "Sorry,the username existed.")
            return redirect("/register")
        elif username=='' or passwd=='' or firstname=='' or lastname=='':
            db.close()
            messages.error(request, "Sorry,the username or passwd or firstname or lastname null.")
            return redirect("/register")
        else:
            cursor.execute(
                """INSERT INTO locations_customuser (password,is_superuser,username , first_name, last_name,email,is_staff,is_active,date_joined,is_operator,balance)
                    VALUES ('{}', '{}', '{}', '{}','{}','{}','{}','{}','{}','{}','{}')""".format(passwd,0,username, firstname,lastname, email,0,0,0,0,0)
            )
            db.commit()
            db.close()
            # return redirect("/login")
            return redirect("/")
    else:
        return render(request, "locations/register.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        passwd = request.POST.get("passwd").strip()

        with sqlite3.connect("./db.sqlite3") as db:
            cursor = db.cursor()
            cursor.execute(
                """SELECT  username, password
                    From locations_customuser
                    WHERE username= '{}' """.format(username)
        )
        res = cursor.fetchone()
        db.close()
        if res:
            if passwd == res[1]:
                return redirect("/")
                # return redirect("/customer")

            else:
                 messages.error(request, "The password is wrong.")
                 # return render(request, "login.html")
                 return redirect("/login")
        else:
            messages.error(request, "The username does not exist.")
            #return render(request, "login.html")
            return redirect("/login")

    # elif request.method == "GET":
    #     return redirect("/register")

    else:
        return render(request, "locations/login.html")


def order_history(request):

    queryset = models.locations_order.objects.all()

    return render(request, 'locations/order_history.html', {'queryset':queryset})