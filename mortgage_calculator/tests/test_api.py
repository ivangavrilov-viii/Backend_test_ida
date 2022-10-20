from collections import OrderedDict

import status
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.utils import json

from mortgage_calculator.models import BankOffer


class TestForms(APITestCase):
    @classmethod
    def setUpTestData(cls):
        BankOffer.objects.create(
            id=4,
            bank_name='First bank',
            term_min=5,
            term_max=15,
            rate_min=8.8,
            rate_max=12.4,
            payment_min=100000,
            payment_max=15000000
        )
        BankOffer.objects.create(
            id=5,
            bank_name='Second bank',
            term_min=1,
            term_max=20,
            rate_min=4.3,
            rate_max=7.9,
            payment_min=1000000,
            payment_max=9000000
        )

    def tearDown(self):
        """Удаление всех данных после тестов"""
        return super().tearDown()

    def test_api_url_exist_at_desired_location(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get(self):
        """Тестирование GET запроса для всех предложений банка"""

        url = reverse('offers-list')
        response = self.client.get(url)
        response_data = [OrderedDict([('id', 5), ('monthly_payment', None), ('bank_name', 'Second bank'),
                                      ('rate_min', 4.3), ('payment_min', 1000000), ('payment_max', 9000000),
                                      ('term_min', 1), ('term_max', 20)]),
                         OrderedDict([('id', 4), ('monthly_payment', None), ('bank_name', 'First bank'),
                                      ('rate_min', 8.8), ('payment_min', 100000), ('payment_max', 15000000),
                                      ('term_min', 5), ('term_max', 15)])]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_data)

    def test_patch(self):
        """Тестирование PATCH запроса на изменение предложения банка"""

        url = reverse('offers-detail', args=[5])
        patch_data = {'bank_name': 'Second bank', 'rate_min': 1, 'payment_min': 1250000,
                      'payment_max': 3000000, 'term_min': 5, 'term_max': 10}
        json_data = json.dumps(patch_data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = {'id': 5, 'monthly_payment': None, 'bank_name': 'Second bank', 'rate_min': 1,
                         'payment_min': 1250000, 'payment_max': 3000000, 'term_min': 5, 'term_max': 10}
        self.assertEqual(response.data, response_data)

    def test_post(self):
        """Тестирование POST запроса на добавление нового предложения"""

        url = reverse('offers-list')
        post_data = {'bank_name': 'Third bank', 'rate_min': 3, 'payment_min': 500000,
                     'payment_max': 5000000, 'term_min': 3, 'term_max': 15}
        json_data = json.dumps(post_data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BankOffer.objects.all().count(), 3)

    def test_delete(self):
        """Тестирование DELETE запроса на удаление предложения"""

        url = reverse('offers-detail', args=[5])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BankOffer.objects.all().count(), 1)

    def test_get_one_offer(self):
        """Тестирование GET запроса для одного предложения банка"""

        url = reverse('offers-detail', args=[5])
        response = self.client.get(url)
        response_data = {'id': 5, 'monthly_payment': None, 'bank_name': 'Second bank', 'rate_min': 4.3,
                         'payment_min': 1000000, 'payment_max': 9000000, 'term_min': 1, 'term_max': 20}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_data)

    def test_with_payments_one_result(self):
        """Тестирование GET запроса с данными для фильтрации с выводом только одного результата"""

        url = reverse('offers-list') + '?price=5000000&deposit=20&term=4'
        response = self.client.get(url)
        response_data = [
            OrderedDict([('id', 5), ('monthly_payment', 113567), ('bank_name', 'Second bank'), ('rate_min', 4.3),
                         ('payment_min', 1000000), ('payment_max', 9000000), ('term_min', 1), ('term_max', 20)])]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_data)

    def test_with_payments_several_result(self):
        """Тестирование GET запроса с данными для фильтрации с выводом только нескольких результатов"""

        url = reverse('offers-list') + '?price=5000000&deposit=20&term=6'
        response = self.client.get(url)
        response_data = [
            OrderedDict([('id', 5), ('monthly_payment', 78911), ('bank_name', 'Second bank'), ('rate_min', 4.3),
                         ('payment_min', 1000000), ('payment_max', 9000000), ('term_min', 1), ('term_max', 20)]),
            OrderedDict([('id', 4), ('monthly_payment', 89632), ('bank_name', 'First bank'), ('rate_min', 8.8),
                         ('payment_min', 100000), ('payment_max', 15000000), ('term_min', 5), ('term_max', 15)])]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_data)

    def test_with_payments_by_order(self):
        """Тестирование сортировки по размеру минимальной ставки по предложениям банков (rate_min)"""

        url = reverse('offers-list') + '?order=rate_min&price=5000000&deposit=20&term=6'
        response = self.client.get(url)
        response_data = [
            OrderedDict([('id', 5), ('monthly_payment', 78911), ('bank_name', 'Second bank'), ('rate_min', 4.3),
                         ('payment_min', 1000000), ('payment_max', 9000000), ('term_min', 1), ('term_max', 20)]),
            OrderedDict([('id', 4), ('monthly_payment', 89632), ('bank_name', 'First bank'), ('rate_min', 8.8),
                         ('payment_min', 100000), ('payment_max', 15000000), ('term_min', 5), ('term_max', 15)])]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_data)

        url = reverse('offers-list') + '?order=-rate_min&price=5000000&deposit=20&term=6'
        response = self.client.get(url)
        response_data = [
            OrderedDict([('id', 4), ('monthly_payment', 89632), ('bank_name', 'First bank'), ('rate_min', 8.8),
                         ('payment_min', 100000), ('payment_max', 15000000), ('term_min', 5), ('term_max', 15)]),
            OrderedDict([('id', 5), ('monthly_payment', 78911), ('bank_name', 'Second bank'), ('rate_min', 4.3),
                         ('payment_min', 1000000), ('payment_max', 9000000), ('term_min', 1), ('term_max', 20)])]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_data)

    def test_base_exception(self):
        with self.assertRaises(BaseException):
            url = reverse('offers-list') + '?price=sdefe&deposit=20&term=6'
            self.client.get(url)
