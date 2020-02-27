from django.db import models

from core.utils import generate_unique_model_id


class Trade(models.Model):
    id = models.AutoField(primary_key=True)
    string_id = models.CharField(max_length=9, unique=True, editable=False, db_index=True)
    sell_currency = models.ForeignKey('Currency', related_name='sell_trades',
                                      on_delete=models.PROTECT, db_index=True)
    sell_amount = models.DecimalField(max_digits=12, decimal_places=2)
    buy_currency = models.ForeignKey('Currency', related_name='buy_trades',
                                     on_delete=models.PROTECT, db_index=True)
    buy_amount = models.DecimalField(max_digits=12, decimal_places=2)
    rate = models.DecimalField(max_digits=9, decimal_places=4)
    date_booked = models.DateTimeField(auto_now_add=True)

    def generate_trade_id(self):
        return generate_unique_model_id(model_class=self.__class__,
                                        prefix='TR', variable_part_length=7)

    def save(self, *args, **kwargs):
        if not self.string_id:
            self.string_id = self.generate_trade_id()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "trades"
        verbose_name = "trade"
        verbose_name_plural = "trades"


class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = "currencies"
        verbose_name = "currency"
        verbose_name_plural = "currencies"
