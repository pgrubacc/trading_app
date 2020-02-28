from unittest.mock import Mock

from rest_framework.exceptions import ValidationError

from django.test import TestCase

from trades.models import Currency
from trades.utils import get_mandatory_query_param, get_currency_query_param


class UtilsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.request = Mock()
        Mock.query_params = {
            'sell': 'EUR',
            'buy': 'Trash'
        }
        cls.sell_currency = Currency.objects.create(name='EUR')

    def test_get_mandatory_query_param(self):
        sell_val = get_mandatory_query_param(self.request, 'sell')
        self.assertEqual(sell_val, Mock.query_params.get('sell'))

    def test_get_mandatory_query_param_invalid(self):
        self.assertRaises(ValidationError, get_mandatory_query_param, self.request, 'nonexistent')

    def test_get_currency_query_param(self):
        sell_currency = get_currency_query_param(self.request, 'sell')
        self.assertEqual(self.sell_currency.name, sell_currency)

    def test_get_invalid_currency_query_param(self):
        self.assertRaises(ValidationError, get_currency_query_param, self.request, 'buy')
