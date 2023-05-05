from django.contrib import admin
from .models import Transaction, Currency, Poll, WalletElement
# Register your models here.

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'buyer', 'currency', 'quantity', 'price')

#class BalanceAdmin(admin.ModelAdmin):
    #list_display = ('user', 'currency_id', 'quantity', 'image', 'balance')

class WalletElementAdmin(admin.ModelAdmin):
    list_display = ('id', 'currency', 'quantity', 'user')

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(WalletElement, WalletElementAdmin)
admin.site.register(Currency)
admin.site.register(Poll)