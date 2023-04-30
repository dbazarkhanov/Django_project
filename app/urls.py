from django.urls import path
from .views import CurrencyList, CurrencyDetail, BalanceList, BalanceDetail, TransactionList, TransactionDetail, PollList, PollDetail

app_name = 'app'

urlpatterns = [
    path('currencies/', CurrencyList.as_view(), name='currency-list'),
    path('currencies/<int:pk>/', CurrencyDetail.as_view(), name='currency-detail'),
    path('balances/', BalanceList.as_view(), name='balance-list'),
    path('balances/<int:pk>/', BalanceDetail.as_view(), name='balance-detail'),
    path('transactions/', TransactionList.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', TransactionDetail.as_view(), name='transaction-detail'),
    path('polls/', PollList.as_view(), name='index'),
    path('polls/<int:pk>/', PollDetail.as_view(), name='poll-detail'),
]
