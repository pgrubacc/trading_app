from unittest.mock import Mock, patch

import responses
from rest_framework.exceptions import ValidationError

from django.conf import settings
from django.test import TestCase

from trades.models import Currency
from trades.utils import get_mandatory_query_param, get_currency_query_param, \
    get_exchange_api_supported_currencies, populate_db_currencies_from_exchange_api


class QueryParamsUtilsTest(TestCase):
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


class ExchangeSupportedCurrenciesUtilsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.exchange_url = f'{settings.EXCHANGE_API_ROOT}/symbols'

    @responses.activate
    def test_get_exchange_supported_currencies(self):
        responses.add(responses.GET, self.exchange_url,
                      json={'success': True,
                            'symbols': {'EUR': 'Euro',
                                        'USD': 'United States Dollar',
                                        'GBP': 'British Pound Sterling'}})
        res = get_exchange_api_supported_currencies()
        expected_response = {'EUR', 'USD', 'GBP'}
        self.assertEqual(res, expected_response)

    def test_populate_db_currencies_from_exchange_api(self):
        expected_currencies = ['EUR', 'GBP', 'USD']
        with patch('trades.utils.get_exchange_api_supported_currencies',
                   return_value=expected_currencies):
            populate_db_currencies_from_exchange_api()
        self.assertEqual(Currency.objects.count(), len(expected_currencies))
