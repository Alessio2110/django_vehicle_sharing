from django.contrib import admin
from .models import Location
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.
admin.site.register(Location)
# admin.site.register(CustomUser, UserAdmin)