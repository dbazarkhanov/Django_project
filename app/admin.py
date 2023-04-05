from django.contrib import admin
from .models import Balance, Transaction, Currency
# Register your models here.

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'user', 'currency_id', 'quantity', 'price', 'to')

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency_id', 'quantity', 'image', 'balance')

admin.site.register(Balance, PortfolioAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Currency)