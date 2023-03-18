import os,django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse,resolve
from locations.views import index,return_order,order_history,order_detail,create_order,conclude_order,deposit,payment

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


