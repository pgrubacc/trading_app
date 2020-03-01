"""
Utility functions for trades app modules.
"""

import requests
from rest_framework.exceptions import ValidationError

from django.conf import settings

from core.exceptions import ServiceUnavailable
from trades.models import Currency


def get_currency_query_param(request, currency):
    """Extracts the value of provided currency query param from request.

    Args:
        request: Django's request object.
        currency: Name of the currency query param.

    Returns:
        Value of the currency query param.

    Raises:
        ValidationError: If the currency is not found in query params or if
        it's not found among Currency objects (lookup by name).

    """
    sell_currency = get_mandatory_query_param(request, currency)
    if not Currency.objects.filter(name=sell_currency).exists():
        raise ValidationError(f'Invalid {currency} currency query param.')
    return sell_currency


def get_mandatory_query_param(request, param):
    """Extracts the value of provided query param from request.

    Args:
        request: Django's request object.
        param: Name of the query param.

    Returns:
        Value of the query param.

    Raises:
        ValidationError: If the currency is not found in query params.

    """
    param_val = request.query_params.get(param)
    if not param_val:
        raise ValidationError(f'Query param {param} is required.')
    return param_val


def get_exchange_rate(sell, buy):
    """Gets the exchange rate between two currencies from the exchange API.

    Args:
        sell: Name of the currency being sold.
        buy: Name of the currency being bought.

    Returns:
       Float exchange rate.

    Raises:
        ServiceUnavailable: If the request towards the API is unsuccessful,
        either due to a network error or its return status.

    """
    rate_endpoint = f'{settings.EXCHANGE_API_ROOT}/latest'
    payload = {
        'access_key': settings.EXCHANGE_API_KEY,
        'base': sell,
        'symbols': buy
    }

    res = perform_exchange_api_request(rate_endpoint, payload)
    return res.get('rates').get(buy)


def exchange_api_response_valid(res):
    """Validates the exchange API response.

    Args:
        res: Dictionary containing response.

    Returns:
       True/False depending on the 'success' field.

    """
    return res.get('success', False)


def get_exchange_api_supported_currencies():
    """Gets currencies supported by the exchange API.

    Returns:
       List of string currency abbreviations.

    Raises:
        ServiceUnavailable: If the request towards the API is unsuccessful,
        either due to a network error or its return status.

    """
    currencies_endpoint = f'{settings.EXCHANGE_API_ROOT}/symbols'
    payload = {'access_key': settings.EXCHANGE_API_KEY}
    res = perform_exchange_api_request(currencies_endpoint, payload)
    return res.get('symbols').keys()


def perform_exchange_api_request(exchange_endpoint, params):
    """Calls an exchange API endpoint.

    Args:
        exchange_endpoint: Exchange string endpoint URL.
        params: Dict containing query params to provide.

    Returns:
       Dict containing response.

    Raises:
        ServiceUnavailable: If the request towards the API is unsuccessful,
        either due to a network error or its return status.

    """
    try:
        res = requests.get(exchange_endpoint, params=params).json()
    except requests.exceptions.RequestException:
        raise ServiceUnavailable('Could not contact the exchange API.')
    if not exchange_api_response_valid(res):
        raise ServiceUnavailable('The exchange api request was unsuccessful.')
    return res


def populate_db_currencies_from_exchange_api():
    """Populates the currency table with currencies retrieved from the exchange API.
       IntegrityErrors due to currencies already existing will be ignored.

    Raises:
        ServiceUnavailable: If the request towards the API is unsuccessful,
        either due to a network error or its return status.

    """
    currencies = get_exchange_api_supported_currencies()
    currency_objs = [Currency(name=currency) for currency in currencies]
    Currency.objects.bulk_create(currency_objs, ignore_conflicts=True)
