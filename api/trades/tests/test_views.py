from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APIClient

from trades.models import Trade, Currency


class TradeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.currency_1 = Currency.objects.create(name='EUR')
        cls.currency_2 = Currency.objects.create(name='USD')

        # create these in a standard way because bulk_create wouldn't trigger save()
        cls.oldest_trade = Trade.objects.create(sell_currency=cls.currency_1, sell_amount=10,
                                                buy_currency=cls.currency_2, buy_amount=15,
                                                rate=1.5,
                                                date_booked=datetime.now() + timedelta(
                                                    seconds=5))
        Trade.objects.create(sell_currency=cls.currency_1, sell_amount=10,
                             buy_currency=cls.currency_2, buy_amount=15, rate=1.5),
        cls.most_recent_trade = Trade.objects.create(sell_currency=cls.currency_1, sell_amount=10,
                                                     buy_currency=cls.currency_2, buy_amount=15,
                                                     rate=1.5,
                                                     date_booked=datetime.now() - timedelta(
                                                         seconds=5))

    def test_get_trades(self):
        res = self.client.get(reverse('trades'))
        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(len(res.data), Trade.objects.count())
        most_recent_result = res.data[0]
        self.assertEqual(most_recent_result['string_id'], self.most_recent_trade.string_id)
        self.assertEqual(most_recent_result['sell_currency'], self.currency_1.name)
        self.assertEqual(most_recent_result['date_booked'],
                         self.most_recent_trade.date_booked.strftime('%d/%m/%Y %H:%M'))
        self.assertEqual(res.data[-1]['string_id'], self.oldest_trade.string_id)

    def test_create_trade(self):
        res = self.client.post(reverse('trades'), data={'sell_currency': self.currency_1.id,
                                                        'sell_amount': 5,
                                                        'buy_currency': self.currency_2.id,
                                                        'buy_amount': 7.5,
                                                        'rate': 1.5})
        self.assertEqual(res.status_code, HTTP_201_CREATED)
        string_id = res.data['string_id']
        self.assertTrue(Trade.objects.filter(string_id=string_id).exists())

    def test_get_currencies(self):
        res = self.client.get(reverse('currencies'))
        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(len(res.data), Currency.objects.count())
        self.assertEqual(res.data[0]['id'], self.currency_1.id)
