import random
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import CustomUser, Location, Vehicle, VehicleType, User

@receiver(post_migrate)
def create_objects(sender, **kwargs):
    if CustomUser.objects.count() == 0:
        # Create objects here
        # CustomUser.objects.create(username='user1', password='password', is_operator=False, balance=10.00)
        # CustomUser.objects.create(username='user2', password='password', is_operator=False, balance=10.00)
        CustomUser.objects.create(user = User.objects.create_user(username = 'user1', password = 'password'), balance = 5)
    if Location.objects.count() == 0:
        # Location.objects.create(address='University of Strathclyde, Glasgow')
        Location.objects.create(address='Kelvinbridge Subway')
        Location.objects.create(address='Kelvinbridge Museum, Glasgow')
        Location.objects.create(address='Glasgow University')
        Location.objects.create(address='Glasgow Central Station')
        # Location.objects.create(address='Glasgow Queen Street, Train Station')
        Location.objects.create(address='Glasgow Caledonian University')
        Location.objects.create(address='Glasgow Royal Infirmary')
        Location.objects.create(address='Glasgow Cathedral')
        Location.objects.create(address='Glasgow Necropolis')
        Location.objects.create(address='Gallery of Modern Art, Glasgow')
        Location.objects.create(address='Glasgow Botanic Gardens')
        Location.objects.create(address='Glasgow Centre for Contemporary Arts')
        Location.objects.create(address='Glasgow Buchanan Galleries')
        Location.objects.create(address='Glasgow St Enoch Shopping Centre')
        Location.objects.create(address='Glasgow Kelvingrove Art Gallery and Museum')
        Location.objects.create(address='Glasgow Science Centre')





    if VehicleType.objects.count() == 0:
        VehicleType.objects.create(name='Bike', cost_per_minute_in_cent = 30, cost_for_initial_order = 50)
        VehicleType.objects.create(name='Scooter', cost_per_minute_in_cent = 40, cost_for_initial_order = 75)

    if Vehicle.objects.count() == 0:
        vehicle_types = list(VehicleType.objects.values_list('id', flat=True))
        locaton_ids = list(Location.objects.values_list('id', flat=True))
        for type in vehicle_types:
            for location in locaton_ids:
                random_number = random.randint(0, 1) # decide on k once
                for _ in range(random_number):
                    Vehicle.objects.create(
                        type = VehicleType.objects.get(id = type),
                        location = Location.objects.get(id = location)
                    )
    

