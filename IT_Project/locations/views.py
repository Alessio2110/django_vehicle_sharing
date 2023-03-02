from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Location

# Create your views here.

class LocationView(CreateView):

    model = Location
    fields = ['address']
    template_name = 'locations/home.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locations'] = Location.objects.all()
        context['mapbox_access_token'] = 'pk.eyJ1IjoiYWxlc3NpbzIxIiwiYSI6ImNsZWszb2twMzBoa3QzcHBnNnhqbHIwMHUifQ.AW2-2b4IYh4qqPqqzMXy8Q'
        return context
