from django.urls import path
# from .views import LocationView
from locations import views

app_name = 'locations'

urlpatterns = [
    path('', views.index, name='index'),
    path('/vehicle', views.index, name='vehicle'),

]
