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
    exchange_endpoint = f'{settings.EXCHANGE_API_ROOT}/latest'
    payload = {
        'access_key': settings.EXCHANGE_API_KEY,
        'base': sell,
        'symbols': buy
    }

    try:
        res = requests.get(exchange_endpoint, params=payload)
    except requests.exceptions.RequestException:
        raise ServiceUnavailable('Could not contact the exchange API.')
    if not validate_exchange_response(res):
        raise ServiceUnavailable('The exchange api request was unsuccessful.')

    return res.json().get('rates').get(buy)


def validate_exchange_response(res):
    return res.json().get('success', False)
