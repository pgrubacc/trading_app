from django.urls import path

import trades.views

urlpatterns = [
    path('trades/', trades.views.TradeList.as_view(), name='trades'),
    path('currencies/', trades.views.CurrencyList.as_view(), name='currencies'),
]
