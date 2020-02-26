from django.contrib import admin

from trades.models import Trade, Currency


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'string_id', 'sell_currency', 'sell_amount',
                    'buy_currency', 'buy_amount', 'rate', 'date_booked', )
    search_fields = ('string_id', 'sell_currency__name', 'buy_currency__name', )


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    search_fields = ('name', )
