from rest_framework import serializers

from trades.models import Trade, Currency


class TradeSerializer(serializers.ModelSerializer):
    sell_currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())
    buy_currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())
    date_booked = serializers.SerializerMethodField()

    class Meta:
        model = Trade
        fields = ('string_id', 'sell_currency', 'sell_amount',
                  'buy_currency', 'buy_amount', 'rate', 'date_booked')

    def get_date_booked(self, obj):
        return obj.date_booked.strftime('%d/%m/%Y %H:%M') if obj.date_booked else None

    def to_representation(self, obj):
        response = super().to_representation(obj)
        response['sell_currency'] = obj.sell_currency.name
        response['buy_currency'] = obj.buy_currency.name
        return response


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('id', 'name',)
