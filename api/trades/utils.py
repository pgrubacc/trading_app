import requests
from rest_framework.exceptions import ValidationError

from django.conf import settings

from trades.exceptions import ServiceUnavailable
from trades.models import Currency


def get_currency_query_param(request, param):
    sell_currency = get_mandatory_query_param(request, param)
    if not Currency.objects.filter(name=sell_currency).exists():
        raise ValidationError(f'Invalid {param} currency query param.')
    return sell_currency


def get_mandatory_query_param(request, param):
    param_val = request.query_params.get(param)
    if not param_val:
        raise ValidationError(f'Query param {param} is required.')
    return param_val


def get_exchange_rate(sell, buy):
    rate_endpoint = f'{settings.EXCHANGE_API_ROOT}/latest'
    payload = {
        'access_key': settings.EXCHANGE_API_KEY,
        'base': sell,
        'symbols': buy
    }

    res = perform_exchange_api_request(rate_endpoint, payload)
    return res.get('rates').get(buy)


def validate_exchange_api_response(res):
    return res.get('success', False)


def get_exchange_api_supported_currencies():
    currencies_endpoint = f'{settings.EXCHANGE_API_ROOT}/symbols'
    payload = {'access_key': settings.EXCHANGE_API_KEY}
    res = perform_exchange_api_request(currencies_endpoint, payload)
    return res.get('symbols').keys()


def perform_exchange_api_request(exchange_endpoint, params):
    try:
        res = requests.get(exchange_endpoint, params=params).json()
    except requests.exceptions.RequestException:
        raise ServiceUnavailable('Could not contact the exchange API.')
    if not validate_exchange_api_response(res):
        raise ServiceUnavailable('The exchange api request was unsuccessful.')
    return res


def populate_db_currencies_from_exchange_api():
    currencies = get_exchange_api_supported_currencies()
    currency_objs = [Currency(name=currency) for currency in currencies]
    Currency.objects.bulk_create(currency_objs, ignore_conflicts=True)
