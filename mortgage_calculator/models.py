from django.db import models
from django.utils.translation import gettext_lazy as _


class BankOffer(models.Model):
    """Модель: предложение по ипотеке"""

    id = models.AutoField(primary_key=True)
    bank_name = models.CharField(max_length=100, verbose_name=_('Bank name'))
    monthly_payment = models.PositiveIntegerField(default=0, verbose_name=_('Monthly payment'))
    term_min = models.PositiveIntegerField(default=1, verbose_name=_('Minimum term'))
    term_max = models.PositiveIntegerField(default=30, verbose_name=_('Maximum term'))
    rate_min = models.FloatField(default=1, verbose_name=_('Minimum rate'))
    rate_max = models.FloatField(default=1, verbose_name=_('Maximum rate'))
    payment_min = models.PositiveIntegerField(default=0, verbose_name=_('Minimum payment'))
    payment_max = models.PositiveIntegerField(verbose_name=_('Maximum payment'))

    class Meta:
        db_table = _('bank_offers')
        verbose_name = _('bank_offer')
        verbose_name_plural = _('bank offers')

    def __str__(self):
        return f'{self.bank_name}'
