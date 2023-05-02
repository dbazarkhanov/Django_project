from django.urls import path
from django.views.generic import TemplateView
from .views import *

app_name = 'app'

urlpatterns = [
    path('main/', TemplateView.as_view(template_name='main.html'), name='main'),
    path('currencies/', CurrencyList.as_view(), name='currency-list'),
    path('balances/', BalanceList.as_view(), name='balance-list'),
    path('transactions/', TransactionList.as_view(), name='transaction-list'),
    path('polls/', PollList.as_view(), name='index'),
]
