from django.contrib import admin
from .models import Balance, Transaction, Currency, Poll
# Register your models here.

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'user', 'currency_id', 'quantity', 'to')

class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency_id', 'quantity', 'image', 'balance')

admin.site.register(Balance, BalanceAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Currency)
admin.site.register(Poll)