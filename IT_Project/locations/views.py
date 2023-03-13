import datetime
import json
import sqlite3
from django.contrib import messages
from django.views.generic.edit import CreateView

from . import models
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import Vehicle, Order, Location, CustomUser, User, VehicleType



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

# Home to make orders
def index(request):
    locations_with_bikes = Location.objects.filter(vehicle__type__name='Bike').distinct() #  all locations that have at least one bike
    locations_with_scooters = Location.objects.filter(vehicle__type__name='Scooter').distinct() # all locations that have at least one scooter

    # Pass data to web page through context
    context = {}
    context['locations_with_bikes'] = locations_with_bikes 
    context['locations_with_scooters'] = locations_with_scooters
    context['mapbox_access_token'] = 'pk.eyJ1IjoiYWxlc3NpbzIxIiwiYSI6ImNsZWszb2twMzBoa3QzcHBnNnhqbHIwMHUifQ.AW2-2b4IYh4qqPqqzMXy8Q' # Mapbox token necessary to use map
    
    return render(request, 'locations/home.html', context=context)

def return_order(request):
    # If user is not logged in, redirect them
    if request.user is None or not request.user.is_authenticated:
        return redirect("/accounts/login")
    # Get customer
    username = request.user.username
    logged_user  = CustomUser.objects.get(user = User.objects.get(username = username))
    # Get order
    unreturned_order = Order.objects.filter(customer = logged_user, final_time = None).first()

    #Pass data to web page through context
    context = {}
    context['order_id'] = unreturned_order.id # Id of the order
    context['initial_time'] = unreturned_order.initial_time.strftime('%Y-%m-%d %H:%M:%S') # Initial time parsed as String
    context['cost_per_minute'] = unreturned_order.vehicle.type.cost_per_minute_in_cent # Cost per minute of the vehicle
    context['cost_for_initial_order'] = unreturned_order.vehicle.type.cost_for_initial_order # Initial cost of renting that vehicle
    context['mapbox_access_token'] = 'pk.eyJ1IjoiYWxlc3NpbzIxIiwiYSI6ImNsZWszb2twMzBoa3QzcHBnNnhqbHIwMHUifQ.AW2-2b4IYh4qqPqqzMXy8Q'  # Mapbox token necessary to use map
    context['locations'] = Location.objects.all() # All locations

    return render(request, 'locations/return.html', context=context)

# def register(request):
#     if request.method == "POST":
#         firstname = request.POST.get("firstname").strip()
#         lastname = request.POST.get("lastname").strip()
#         username = request.POST.get("username").strip()
#         passwd = request.POST.get("passwd").strip()
#         email =  request.POST.get("email").strip()

#         with sqlite3.connect("./db.sqlite3") as db:
#             cursor = db.cursor()
#             cursor.execute(
#             """SELECT username
#                     From locations_customuser
#                     WHERE username= '{}' """.format(username)
#         )
#         res = cursor.fetchone()
#         if res:
#             db.close()
#             messages.error(request, "Sorry,the username existed.")
#             return redirect("/register")
#         elif username=='' or passwd=='' or firstname=='' or lastname=='':
#             db.close()
#             messages.error(request, "Sorry,the username or passwd or firstname or lastname null.")
#             return redirect("/register")
#         else:
#             cursor.execute(
#                 """INSERT INTO locations_customuser (password,is_superuser,username , first_name, last_name,email,is_staff,is_active,date_joined,is_operator,balance)
#                     VALUES ('{}', '{}', '{}', '{}','{}','{}','{}','{}','{}','{}','{}')""".format(passwd,0,username, firstname,lastname, email,0,0,0,0,0)
#             )
#             db.commit()
#             db.close()
#             # return redirect("/login")
#             return redirect("/")
#     else:
#         return render(request, "locations/register.html")

# def login(request):
#     if request.method == "POST":
#         username = request.POST.get("username").strip()
#         passwd = request.POST.get("passwd").strip()

#         with sqlite3.connect("./db.sqlite3") as db:
#             cursor = db.cursor()
#             cursor.execute(
#                 """SELECT  username, password
#                     From locations_customuser
#                     WHERE username= '{}' """.format(username)
#         )
#         res = cursor.fetchone()
#         db.close()
#         if res:
#             if passwd == res[1]:
#                 return redirect("/")
#                 # return redirect("/customer")

#             else:
#                  messages.error(request, "The password is wrong.")
#                  # return render(request, "login.html")
#                  return redirect("/login")
#         else:
#             messages.error(request, "The username does not exist.")
#             #return render(request, "login.html")
#             return redirect("/login")

#     # elif request.method == "GET":
#     #     return redirect("/register")

#     else:
#         return render(request, "locations/login.html")


# from django.contrib.auth import authenticate, login

# def login(request):
#     if request.method == "POST":
#         username = request.POST.get("username").strip()
#         password = request.POST.get("passwd").strip()
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect("/")
#         else:
#             messages.error(request, "Invalid username or password.")
#             return redirect("/login")
#     else:
#         return render(request, "locations/login.html")


def order_history(request):

    queryset = models.Order.objects.all()

    return render(request, 'locations/order_history.html', {'queryset':queryset})

def order_detail(request,nid):

    queryset = models.Order.objects.filter(id=nid)

    return render(request, 'locations/order_detail.html', {'queryset':queryset})

# Create new order given data from user
def create_order(request):
    # Redirect if not a post
    if request.method != 'POST':
        return render(request, 'locations/home.html')
    # Get data from json
    data = json.loads(request.body)
    username = data['username']
    vehicle_type = data['vehicle_type']
    loc_id = data['loc_id']

    # Get customer, locations and update vehicle's availability
    user = CustomUser.objects.get(user = User.objects.get(username = username))
    location = Location.objects.get(id=loc_id)
    vehicle = Vehicle.objects.filter(is_available = True, location=location, type = VehicleType.objects.get(name = vehicle_type)).order_by('id').first()
    vehicle.is_available = False
    vehicle.save()

    # Create order
    order = Order.objects.create(
        customer = user,
        vehicle = vehicle,
        initial_location = location
    )
    # Succesful response
    return JsonResponse({'status': 'success'})

# Terminate order and update fields
def conclude_order(request):
    # If not a post, redirect
    if request.method != 'POST':
        return render(request, '{locations:return_order}')
    # Get data from JSON
    data = json.loads(request.body)
    loc_id = data['loc_id']
    order_id = data['order_id']
    order = Order.objects.get(id = order_id)

    # Get vehicle and update location and availability
    used_vehicle = order.vehicle
    used_vehicle.is_available = True
    used_vehicle.location = Location.objects.get(id = loc_id)
    used_vehicle.save()

    # Add order location and final time
    order.final_location = Location.objects.get(id = loc_id)
    order.final_time = datetime.datetime.now()

    # Calculate duration and cost
    duration = order.initial_time - order.final_time 
    duration_in_seconds = duration.total_seconds()
    duration_in_minutes = int(duration_in_seconds / 60)
    order.cost = (duration_in_minutes * order.vehicle.type.cost_per_minute_in_cent + order.vehicle.type.cost_for_initial_order) / 100

    # Save
    order.save()

    return JsonResponse({'status': 'success'})


    

    





    

