from django.db import models
import geocoder
from django.contrib.auth.models import AbstractUser
# IMPORTANT!
# Models are not finished!

MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiYWxlc3NpbzIxIiwiYSI6ImNsZWszb2twMzBoa3QzcHBnNnhqbHIwMHUifQ.AW2-2b4IYh4qqPqqzMXy8Q'

class Location(models.Model):
    address = models.TextField()
    latitude = models.FloatField(blank = True, null = True)
    longitude = models.FloatField(blank = True, null = True)

    def save(self, *args, **kwargs):
        #Get the geocoder object relative to the provided address
        g = geocoder.mapbox(self.address, key = MAPBOX_ACCESS_TOKEN)
        #Get the longitude and latitude of the location
        g = g.latlng 
        self.latitude, self.longitude = g[0], g[1]
        return super(Location, self).save(*args, **kwargs)

class CustomUser(AbstractUser):
    is_operator = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=6, decimal_places=2,default=10.00)

    def is_an_operator(self):
        return self.is_operator

    def is_a_customer(self):
        return not self.is_operator
    
    def __str__(self):
        return self.username

class VehicleType(models.Model):
    name = models.CharField(max_length=10)
    cost_per_minute_in_cent = models.IntegerField(default= 30)
    cost_for_initial_order = models.IntegerField(default = 50)
    def __str__(self):
        return self.name
    
class Vehicle(models.Model):
    type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    
class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    initial_time = models.TimeField(auto_now_add=True)
    final_time = models.TimeField()
    initial_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=False, related_name='start')
    final_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, related_name='end')
    is_paid = models.BooleanField(default=False)

class Report(models.Model):
    text = models.TextField(max_length="255")
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
class ReportType(models.Model):
    report_type = models.TextField(max_length="63", default="Other issues")


# The ones below this line are the tables concerning operators
# Operators will likely not be included in the project, so ignore them!

# Probably not going to be used
class Repair(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    operator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)




