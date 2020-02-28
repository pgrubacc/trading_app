from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from trades.models import Trade, Currency
from trades.serializers import TradeSerializer, CurrencySerializer
from trades.utils import get_currency_query_param, get_exchange_rate


class TradeList(ListCreateAPIView):
    queryset = Trade.objects.select_related('sell_currency', 'buy_currency').\
        order_by('-date_booked')
    serializer_class = TradeSerializer


class CurrencyList(ListAPIView):
    queryset = Currency.objects.order_by('name')
    serializer_class = CurrencySerializer


class ExchangeRate(APIView):
    def get(self, request):
        sell_currency = get_currency_query_param(request, 'sell')
        buy_currency = get_currency_query_param(request, 'buy')
        rate = get_exchange_rate(sell_currency, buy_currency)
        return Response({'rate': round(rate, 4) if rate is not None else 0},
                        status=HTTP_200_OK)
