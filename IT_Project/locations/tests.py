import os
import django
import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()
from datetime import datetime, timedelta
from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse,resolve
from django.utils import timezone
from locations.views import index, return_order, order_history, order_detail, create_order, conclude_order, deposit, payment
from django.contrib.auth.models import User
from decimal import Decimal
from django.test import Client
from locations.models import Location, CustomUser, VehicleType, Vehicle, Order, ReportType, Report
import json
from django.core.exceptions import ValidationError

from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import CustomUser, Location, VehicleType, Vehicle, Order
from decimal import Decimal

class LocationTstCase(TestCase):
    def setUp(self):
        Location.objects.create(address="123 Main St")

    def test_location_creation(self):
        location = Location.objects.get(address="123 Main St")
        location.save()
        self.assertEqual(location.latitude, 55.711955)
        self.assertEqual(location.longitude, -4.540292)

class CustomUserTestCase(TestCase):
    def setUp(self):
        user, created = User.objects.get_or_create(username='testuser')
        if created:
            user.set_password('testpassword')
            user.save()

        custom_user, created = CustomUser.objects.get_or_create(user=user, defaults={'balance': 50.00})
        if not created:
            custom_user.balance = 50.00
            custom_user.save()

    def test_custom_user_creation(self):
        custom_user = CustomUser.objects.get(user__username="testuser")
        self.assertEqual(custom_user.balance, 50.00)

class VehicleTypeTestCase(TestCase):
    def setUp(self):
        vehicle_type, created = VehicleType.objects.get_or_create(
            name="Scooter",
            defaults={"cost_per_minute_in_cent": 30, "cost_for_initial_order": 50},
        )
        if not created:
            vehicle_type.cost_per_minute_in_cent = 30
            vehicle_type.cost_for_initial_order = 50
            vehicle_type.save()
    def test_vehicle_type_creation(self):
        vehicle_type = VehicleType.objects.get(name="Scooter")
        self.assertEqual(vehicle_type.cost_per_minute_in_cent, 30)
        self.assertEqual(vehicle_type.cost_for_initial_order, 50)

class VehicleTestCase(TestCase):
    def setUp(self):
        vehicle_type, created = VehicleType.objects.get_or_create(
            name="Bike",
            defaults={"cost_per_minute_in_cent": 20, "cost_for_initial_order": 40},
        )
        if not created:
            vehicle_type.cost_per_minute_in_cent = 20
            vehicle_type.cost_for_initial_order = 40
            vehicle_type.save()

        location, _ = Location.objects.get_or_create(
            address="124 Main St",
            latitude=55.95,
            longitude=-4.15,
        )

        Vehicle.objects.create(type=vehicle_type, location=location)

    def test_vehicle_creation(self):
        vehicle = Vehicle.objects.get(location__address="124 Main St")
        self.assertEqual(vehicle.type.name, "Bike")
        self.assertTrue(vehicle.is_available)

class OrderTestCase(TestCase):
    def setUp(self):
        user, created = User.objects.get_or_create(username='testuser')
        if created:
            user.set_password('testpassword')
            user.save()

        custom_user, created = CustomUser.objects.get_or_create(user=user, defaults={'balance': 50.00})
        if not created:
            custom_user.balance = 50.00
            custom_user.save()
        vehicle_type, created = VehicleType.objects.get_or_create(
            name="Bike",
            defaults={"cost_per_minute_in_cent": 20, "cost_for_initial_order": 40},
        )
        if not created:
            vehicle_type.cost_per_minute_in_cent = 20
            vehicle_type.cost_for_initial_order = 40
            vehicle_type.save()

        location, _ = Location.objects.get_or_create(
            address="124 Main St",
            latitude=55.95,
            longitude=-4.15,
        )

        Vehicle.objects.create(type=vehicle_type, location=location)
        vehicle = Vehicle.objects.create(type=vehicle_type, location=location)
        initial_location = Location.objects.create(address="125 Main St", latitude=55.90, longitude=-4.10)
        Order.objects.create(customer=custom_user, vehicle=vehicle, cost=20.00, initial_location=initial_location)

    def test_order_creation(self):
        order = Order.objects.get(customer__user__username="testuser")
        self.assertEqual(order.vehicle.type.name, "Bike")
        self.assertEqual(order.cost, 20.00)
        self.assertEqual(order.initial_location.address, "125 Main St")

class ReportTypeTestCase(TestCase):
    def setUp(self):
        ReportType.objects.create(report_type="Damaged vehicle")

    def test_report_type_creation(self):
        report_type = ReportType.objects.get(report_type="Damaged vehicle")
        self.assertEqual(report_type.report_type, "Damaged vehicle")

class ReportTestCase(TestCase):
    def setUp(self):
        user, created = User.objects.get_or_create(username='testuser')
        if created:
            user.set_password('testpassword')
            user.save()

        custom_user, created = CustomUser.objects.get_or_create(user=user, defaults={'balance': 50.00})
        if not created:
            custom_user.balance = 50.00
            custom_user.save()
        vehicle_type, created = VehicleType.objects.get_or_create(
            name="Bike",
            defaults={"cost_per_minute_in_cent": 20, "cost_for_initial_order": 40},
        )
        if not created:
            vehicle_type.cost_per_minute_in_cent = 20
            vehicle_type.cost_for_initial_order = 40
            vehicle_type.save()

        location, _ = Location.objects.get_or_create(
            address="124 Main St",
            latitude=55.95,
            longitude=-4.15,
        )

        Vehicle.objects.create(type=vehicle_type, location=location)
        vehicle = Vehicle.objects.create(type=vehicle_type, location=location)
        initial_location = Location.objects.create(address="125 Main St", latitude=55.90, longitude=-4.10)
        order = Order.objects.create(customer=custom_user, vehicle=vehicle, cost=20.00, initial_location=initial_location)
        report_type = ReportType.objects.create(report_type="Damaged vehicle")
        Report.objects.create(text="Flat tire", order=order, report_type=report_type)

    def test_report_creation(self):
        report = Report.objects.get(order__customer__user__username="testuser")
        self.assertEqual(report.text, "Flat tire")
        self.assertEqual(report.order.vehicle.type.name, "Bike")
        self.assertEqual(report.report_type.report_type, "Damaged vehicle")


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        # Create test users
        self.user1, _ = User.objects.get_or_create(username='testuser1', defaults={'password': 'testpassword1'})
        self.user1.set_password('testpassword1')
        self.user1.save()
        self.custom_user1, _ = CustomUser.objects.get_or_create(user=self.user1, defaults={'balance': 100})

        self.user2, _ = User.objects.get_or_create(username='testuser2', defaults={'password': 'testpassword2'})
        self.user2.set_password('testpassword2')
        self.user2.save()
        self.custom_user2, _ = CustomUser.objects.get_or_create(user=self.user2, defaults={'balance': 150})

        # Create test vehicle types
        self.bike, _ = VehicleType.objects.get_or_create(name='Bike', defaults={'cost_per_minute_in_cent': 10,
                                                                                'cost_for_initial_order': 100})
        self.scooter, _ = VehicleType.objects.get_or_create(name='Scooter', defaults={'cost_per_minute_in_cent': 15,
                                                                                      'cost_for_initial_order': 150})
        # Create test locations
        self.location1 = Location.objects.create(address='123 Test St', latitude=1.234, longitude=2.345)
        self.location2 = Location.objects.create(address='456 Test Ave', latitude=3.456, longitude=4.567)

        # Create test vehicles
        self.vehicle1 = Vehicle.objects.create(is_available=True, location=self.location1, type=self.bike)
        self.vehicle2 = Vehicle.objects.create(is_available=True, location=self.location2, type=self.scooter)

        # Create test orders
        self.order1 = Order.objects.create(customer=self.custom_user1, vehicle=self.vehicle1,
                                           initial_location=self.location1)
        self.order2 = Order.objects.create(customer=self.custom_user2, vehicle=self.vehicle2,
                                           initial_location=self.location2)
        self.order1.final_location = self.location1
        self.order1.save()

        self.order2.final_location = self.location2
        self.order2.save()

        self.order1.final_time = None
        self.order1.save()

        self.order2.final_time = timezone.now()
        self.order2.save()


        self.order1.cost = Decimal('10.00')
        self.order1.save()

        self.order2.cost = Decimal('20.00')
        self.order2.save()
    def test_index(self):
        response = self.client.get(reverse('locations:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'locations/home.html')

    def test_return_order_authenticated(self):
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.get(reverse('locations:return_order'))
        self.assertContains(response, f"{self.order1.id}")

    def test_return_order_unauthenticated(self):
        response = self.client.get(reverse('locations:return_order'))

        self.assertEqual(response.status_code, 302)
    def test_order_history_authenticated(self):
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.get(reverse('locations:order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'locations/order_history.html')

    def test_order_history_unauthenticated(self):
        response = self.client.get(reverse('locations:order_history'))

        def test_order_history_unauthenticated(self):
            response = self.client.get(reverse('locations:order_history'))
            self.assertRedirects(response, '/accounts/login?next=/order_history/', status_code=301,
                                 target_status_code=302)

    def test_order_detail_unauthenticated(self):
        response = self.client.get(reverse('locations:order_detail', args=[self.order1.id]))

        def test_order_detail_unauthenticated(self):
            response = self.client.get(reverse('locations:order_detail'))
            self.assertRedirects(response, '/accounts/login?next=/order_detail/', status_code=301, target_status_code=302)

    def test_order_detail_wrong_user(self):
        self.client.login(username='testuser2', password='testpassword2')
        self.order1.final_time = timezone.now()
        self.order1.save()
        response = self.client.get(reverse('locations:order_detail', args=[self.order1.id]))
        self.assertRedirects(response, '/order_history/')

    def test_create_order(self):
        self.client.login(username='testuser1', password='testpassword1')
        data = {
            'username': 'testuser1',
            'vehicle_type': 'Bike',
            'loc_id': self.location1.id
        }
        response = self.client.post(reverse('locations:create_order'), json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')

    def test_conclude_order(self):
        self.client.login(username='testuser1', password='testpassword1')
        data = {
            'loc_id': self.location2.id,
            'order_id': self.order1.id
        }
        response = self.client.post(reverse('locations:conclude_order'), json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')

    def test_deposit_authenticated(self):
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.get(reverse('locations:deposit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'locations/deposit.html')

    def test_deposit_unauthenticated(self):
        response = self.client.get(reverse('locations:deposit'))

        def test_deposit_unauthenticated(self):
            response = self.client.get(reverse('locations:deposit'))
            self.assertRedirects(response, '/accounts/login?next=/deposit/', status_code=301, target_status_code=302)

    def test_payment_authenticated(self):
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.get(reverse('locations:payment', args=[self.order1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'locations/payment.html')

    def test_payment_unauthenticated(self):
        response = self.client.get(reverse('locations:payment', args=[self.order1.id]))

        def test_payment_unauthenticated(self):
            response = self.client.get(reverse('locations:payment'))
            self.assertRedirects(response, '/accounts/login?next=/payment/', status_code=301, target_status_code=302)

    def test_payment_wrong_user(self):
        self.client.login(username='testuser2', password='testpassword2')
        response = self.client.get(reverse('locations:payment', args=[self.order1.id]))
        self.assertRedirects(response, '/order_history/')

    def test_payment_post_success(self):
        self.client.login(username='testuser2', password='testpassword2')
        response = self.client.post(reverse('locations:payment', args=[self.order2.id]))
        self.assertRedirects(response, '/deposit/')
        self.order2.refresh_from_db()
        self.assertFalse(self.order2.is_paid)

    def test_payment_post_insufficient_balance(self):
        self.client.login(username='testuser2', password='testpassword2')
        response = self.client.post(reverse('locations:payment', args=[self.order2.id]))
        self.assertRedirects(response, '/deposit/')

    def test_payment_already_paid(self):
        self.client.login(username='testuser1', password='testpassword1')
        self.order1.is_paid = True
        self.order1.save()
        response = self.client.get(reverse('locations:payment', args=[self.order1.id]))
        self.assertRedirects(response, '/order_history/')

