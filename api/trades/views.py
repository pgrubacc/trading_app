from rest_framework.generics import ListCreateAPIView, ListAPIView

from trades.models import Trade, Currency
from trades.serializers import TradeSerializer, CurrencySerializer


class TradeList(ListCreateAPIView):
    queryset = Trade.objects.select_related('sell_currency', 'buy_currency').\
        order_by('-date_booked')
    serializer_class = TradeSerializer


class CurrencyList(ListAPIView):
    queryset = Currency.objects.order_by('name')
    serializer_class = CurrencySerializer
