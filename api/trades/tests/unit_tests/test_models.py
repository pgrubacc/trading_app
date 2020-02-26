from django.test import TestCase
from unittest.mock import patch

from trades.models import Currency, Trade


class TradeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.unique_id = 'TR1234567'
        cls.sell_currency = Currency.objects.create(name='USD')
        cls.buy_currency = Currency.objects.create(name='USD')
        Trade.objects.create(string_id=cls.unique_id, sell_currency=cls.sell_currency,
                             sell_amount=10, buy_currency=cls.buy_currency, buy_amount=15, rate=1.5)

    def test_id_uniqueness(self):
        available_id = '1234ASD'
        with patch('core.utils.generate_random_alphanumeric',
                   side_effect=[self.unique_id.strip('TR'), available_id]) as mock_id_randomness:
            Trade.objects.create(sell_currency=self.sell_currency, sell_amount=10,
                                 buy_currency=self.buy_currency, buy_amount=20, rate=2)
            self.assertEqual(mock_id_randomness.call_count, 2)
        self.assertEqual(Trade.objects.count(), 2)
