import datetime
import json
import sqlite3
from django.contrib import messages
from django.views.generic.edit import CreateView
from decimal import Decimal

from . import models
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import Vehicle, Order, Location, CustomUser, User, VehicleType



from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

# Create your views here.
# Persona acess token to use mapbox
ACCESS_TOKEN_MAPBOX = 'pk.eyJ1IjoiYWxlc3NpbzIxIiwiYSI6ImNsZWszb2twMzBoa3QzcHBnNnhqbHIwMHUifQ.AW2-2b4IYh4qqPqqzMXy8Q'

# View to start a new order
def index(request):
    locations_with_bikes = Location.objects.filter(vehicle__type__name='Bike', vehicle__is_available = True).distinct() #  all locations that have at least one bike
    locations_with_scooters = Location.objects.filter(vehicle__type__name='Scooter', vehicle__is_available = True).distinct() # all locations that have at least one scooter
    bike = VehicleType.objects.get(name = "Bike")
    scooter = VehicleType.objects.get(name = "Scooter")

    # Pass data to web page through context
    context = {}
    context['locations_with_bikes'] = locations_with_bikes 
    context['locations_with_scooters'] = locations_with_scooters
    context['mapbox_access_token'] = ACCESS_TOKEN_MAPBOX # Mapbox token necessary to use map
    context['bike'] = bike
    context['scooter'] = scooter

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
    context['mapbox_access_token'] = ACCESS_TOKEN_MAPBOX  # Mapbox token necessary to use map
    context['locations'] = Location.objects.all() # All locations

    return render(request, 'locations/return.html', context=context)

def order_history(request):
    if request.user is None or not request.user.is_authenticated:
        return redirect("/accounts/login")

    username = request.user.username
    logged_customer = CustomUser.objects.get(user=User.objects.get(username=username))
    queryset = models.Order.objects.filter(customer=logged_customer).order_by('id').reverse()

    return render(request, 'locations/order_history.html', {'queryset': queryset})

def order_detail(request,nid):
    #If user it not authenticated, redirect to login
    if request.user is None or not request.user.is_authenticated:
        return redirect("/accounts/login")
    #Get data
    order = models.Order.objects.get(id=nid)
    vehicle = order.vehicle.type.name
    date = order.initial_time.date()
    # Calculate duration
    return_time = order.final_time.strftime("%H:%M")
    timedelta = order.final_time - order.initial_time
    hours, remainder = divmod(timedelta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    cost = order.cost
    # From ---> to
    initial_address = order.initial_location.address
    final_address = order.final_location.address
    # If not the same customer, redirect
    if order.customer.user != request.user:
        return redirect("/order_history/")

    obj={'vehicle': vehicle , 'order_id':nid, 'date': date , 'returntime':return_time , 'formatted_time': formatted_time , 'cost':cost , 'iadd':initial_address , 'fadd':final_address, 'is_paid': order.is_paid}

    return render(request, 'locations/order_detail.html', {'obj': obj})

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
    duration = order.final_time - order.initial_time
    duration_in_seconds = duration.total_seconds()
    duration_in_minutes = int(duration_in_seconds / 60)
    order.cost = (duration_in_minutes * order.vehicle.type.cost_per_minute_in_cent + order.vehicle.type.cost_for_initial_order) / 100

    # Save
    order.save()

    return JsonResponse({'status': 'success'})


def deposit(request):
    #If user is logged in
    if request.user is None or not request.user.is_authenticated:
        return redirect("/accounts/login")
    username = request.user.username
    logged_customer = CustomUser.objects.get(user=User.objects.get(username=username))
    # If button clicked
    if request.method == "POST":
        depositAmount = Decimal(request.POST.get("depositAmount"))
        logged_customer.balance += depositAmount
        logged_customer.save()
        return redirect("/order_history/")
    else:
        context = {}
        context['customer'] = logged_customer
        return render(request, "locations/deposit.html", context = context)
    

def payment(request,nid):
    #If user is not logged in, redirect
    if request.user is None or not request.user.is_authenticated:
        return redirect("/accounts/login")

    username = request.user.username
    logged_customer = CustomUser.objects.get(user=User.objects.get(username=username))
    balance = logged_customer.balance
    order = models.Order.objects.get(id=nid)
    cost=order.cost
    # Update balance
    if request.method == "POST":
        if(balance>cost):
            order.is_paid=1
            order.save()
            logged_customer.balance -= cost
            logged_customer.save()
            return redirect("/order_history/")
        else:
            return redirect("/deposit/")
    # If paid, go to order history
    if order.is_paid:
       return redirect("/order_history/")
    
    if order.customer.user.username != logged_customer.user.username:
        return redirect("/order_history/")

    context={'balance':balance , 'cost':cost, 'order': order}

    return render(request, "locations/payment.html", context)
