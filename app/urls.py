from django.urls import path
from .views import *


app_name = 'app'

urlpatterns = [
    path('currencies/', CurrencyList.as_view(), name='currency-list'),
    # path('currencies/<int:id>/', CurrencyDetail.as_view(), name='currency-detail'),
    path('transactions/', TransactionList.as_view(), name='transaction-list'),
    # path('transactions/<int:id>/', TransactionDetail.as_view(), name='transaction-detail'),
    path('polls/', PollList.as_view(), name='offers'),
    # path('polls/<int:id>/', PollDetail.as_view(), name='poll-detail'),

]
