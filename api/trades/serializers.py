from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from trades.models import Trade, Currency


class TradeSerializer(serializers.ModelSerializer):
    sell_currency = serializers.SlugRelatedField(slug_field='name', queryset=Currency.objects.all())
    buy_currency = serializers.SlugRelatedField(slug_field='name', queryset=Currency.objects.all())
    date_booked = serializers.SerializerMethodField()

    class Meta:
        model = Trade
        fields = ('string_id', 'sell_currency', 'sell_amount',
                  'buy_currency', 'buy_amount', 'rate', 'date_booked')

    def get_date_booked(self, obj):
        return obj.date_booked.strftime('%d/%m/%Y %H:%M') if obj.date_booked else None

    def validate(self, data):
        if data['sell_currency'] == data['buy_currency']:
            raise ValidationError('Sell and buy currency values cannot be identical.')
        return data


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('name',)
