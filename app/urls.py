from django.urls import path
from django.views.generic import TemplateView
from .views import *

app_name = 'app'

urlpatterns = [
    path('main/', TemplateView.as_view(template_name='main.html'), name='main'),
    # path('currencies/', CurrencyList.as_view(), name='currency-list'),
    # # path('currencies/<int:id>/', CurrencyDetail.as_view(), name='currency-detail'),
    # path('balances/', BalanceList.as_view(), name='balance-list'),
    # # path('balances/<int:id>/', BalanceDetail.as_view(), name='balance-detail'),
    # path('transactions/', TransactionList.as_view(), name='transaction-list'),
    # # path('transactions/<int:id>/', TransactionDetail.as_view(), name='transaction-detail'),
    # path('polls/', PollList.as_view(), name='index'),
    # # path('polls/<int:id>/', PollDetail.as_view(), name='poll-detail'),
]
