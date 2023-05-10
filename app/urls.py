from django.urls import path
from django.views.generic import TemplateView
from .views import *


app_name = 'app'

urlpatterns = [
    path('', TemplateView.as_view(template_name='main.html'), name='main'),
    path('api/currencies/', CurrencyList.as_view(), name='currency_list'),
    path('currencies/', CurrencyView.as_view(), name='currency-list-view'),
    path('currencies/<int:id>/', CurrencyDetail.as_view(), name='currency-detail'),
    path('transactions/', TransactionList.as_view(), name='transaction-list'),
    path('polls/', PollList.as_view(), name='offers'),
    path('polls/<int:id>/', PollList.as_view(), name='my-offers'),

    path('buyOffer/', BuyHandler.as_view(), name='buy-offer'),
    path('sellOffer/', SellHandler.as_view(), name='sell-offer'),
    path('deleteOffer/<int:id>', DeleteHandler.as_view(), name='delete-offer'),
]
