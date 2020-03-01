from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from trades.models import Trade, Currency
from trades.serializers import TradeSerializer, CurrencySerializer
from trades.utils import get_currency_query_param, get_exchange_rate


class TradeList(ListCreateAPIView):
    """
    View used to list and create trades.

    get:
    Gets the list of trades sorted by date booked, descending.

    post:
    Creates a new trade.
    """
    queryset = Trade.objects.select_related('sell_currency', 'buy_currency').\
        order_by('-date_booked')
    serializer_class = TradeSerializer


class CurrencyList(ListAPIView):
    """
    Get the list of supported currencies, sorted by name.
    """
    queryset = Currency.objects.order_by('name')
    serializer_class = CurrencySerializer


class ExchangeRate(APIView):
    """
    Get the exchange rate between two currencies.
     Parameters:
        sell - name of the currency being sold (MANDATORY, name must exist in the currency table)
        buy - name of the currency being bought (MANDATORY, name must exist in the currency table)

    http://localhost:8002/api/v1.0/rates/?sell=EUR&buy=USD
    """
    def get(self, request):
        sell_currency = get_currency_query_param(request, 'sell')
        buy_currency = get_currency_query_param(request, 'buy')
        rate = get_exchange_rate(sell_currency, buy_currency)
        return Response({'rate': round(rate, 4) if rate is not None else 0},
                        status=HTTP_200_OK)
