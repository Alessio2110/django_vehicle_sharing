from django.urls import path
from .views import LocationView

app_name = 'location'

urlpatterns = [
    path('', LocationView.as_view(), name='home')
]
