import os,django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse,resolve
from locations.views import index,return_order,order_history,order_detail,create_order,conclude_order,deposit,payment
from django.contrib.auth.models import User

from django.test import Client
from locations.models import Location, CustomUser, VehicleType, Vehicle, Order, ReportType, Report
import json


class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_return_order_url_is_resolved(self):
        url = reverse('return_order')
        self.assertEquals(resolve(url).func, return_order)

    def test_order_history_is_resolved(self):
        url = reverse('order_history')
        self.assertEquals(resolve(url).func, order_history)

    def test_order_detail_url_is_resolved(self):
        url = reverse('order_detail', args=1)
        self.assertEquals(resolve(url).func, order_detail)

    def test_create_order_is_resolved(self):
        url = reverse('create_order')
        self.assertEquals(resolve(url).func, create_order)

    def test_conclude_order_url_is_resolved(self):
        url = reverse('conclude_order')
        self.assertEquals(resolve(url).func, conclude_order)

    def test_deposit_url_is_resolved(self):
        url = reverse('deposit')
        self.assertEquals(resolve(url).func, deposit)

    def test_payment_url_is_resolved(self):
        url = reverse('payment', args=1)
        self.assertEquals(resolve(url).func, payment)


class TestViews(TestCase):


    def test_index_GET(self):
        client = Client()
        response = client.get(reverse('index'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'locations/home.html')


    def test_return_order_REDIRECT(self):
        client = Client()
        response = client.get(reverse('return_order'))

        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed(response, '/accounts/login')

    def test_return_order_GET(self):
        client = Client()
        client.user = User()
        client.user.is_authenticated = True
        client.user.username = "user1"

        response = client.get(reverse('return_order'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'locations/return.html')

    def test_order_history_REDIRECT(self):
        client = Client()
        response = client.get(reverse('order_history'))

        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed(response, '/accounts/login')

    def test_order_history_GET(self):
        client = Client()
        client.user = User()
        client.user.is_authenticated = True
        client.user.username = "user1"

        response = client.get(reverse('order_history'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'locations/order_history.html')


class LocationModelTestCase(TestCase):

    def test_location_save_method(self):
        # Create a location instance with a known address
        location = Location.objects.create(address='1600 Amphitheatre Parkway, Mountain View, CA')

        # Assert that the latitude and longitude were set correctly
        self.assertAlmostEqual(location.latitude, 37.4219999, delta=0.01)
        self.assertAlmostEqual(location.longitude, -122.0840575, delta=0.01)


class CustomUserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.custom_user = CustomUser.objects.create(
            user=self.user,
            balance=20.00
        )

    def test_is_a_customer(self):
        self.assertTrue(self.custom_user.is_a_customer())

    def test_str(self):
        self.assertEqual(str(self.custom_user), 'testuser')


class VehicleTypeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a VehicleType object for testing
        VehicleType.objects.create(name='Car', cost_per_minute_in_cent=50, cost_for_initial_order=100)

    def test_vehicle_type_str_method(self):
        # Test the __str__ method of the VehicleType model
        vehicle_type = VehicleType.objects.get(id=1)
        self.assertEqual(str(vehicle_type), 'Car')

    def test_vehicle_type_defaults(self):
        # Test the default values of the cost_per_minute_in_cent and cost_for_initial_order fields
        vehicle_type = VehicleType.objects.get(id=1)
        self.assertEqual(vehicle_type.cost_per_minute_in_cent, 50)
        self.assertEqual(vehicle_type.cost_for_initial_order, 100)



