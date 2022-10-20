from django.contrib import admin

from .models import BankOffer


class BankOfferAdmin(admin.ModelAdmin):
    list_display = ['id', 'bank_name', 'term_min', 'term_max', 'rate_min', 'rate_max', 'payment_min', 'payment_max']


admin.site.register(BankOffer, BankOfferAdmin)
