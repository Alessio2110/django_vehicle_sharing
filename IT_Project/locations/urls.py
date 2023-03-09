from django.urls import path
# from .views import LocationView
from locations import views

app_name = 'location'

urlpatterns = [
    path('', views.index, name='home'),
    path('/vehicle', views.index, name='vehicle'),
    path('<int:customer_id>/', views.order_history, name='order_history'),

]
