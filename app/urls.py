from django.urls import path
from django.views.generic import TemplateView
from .views import *


app_name = 'app'

urlpatterns = [
    path('', TemplateView.as_view(template_name='main.html'), name='main'),
    path('api/currencies/', CurrencyList.as_view(), name='currency_api'),
    path('currencies/', CurrencyView.as_view(), name='crypt'),
    path('currencies/<int:id>/', CurrencyDetail.as_view(), name='b_details'),
    # path('transactions/', TransactionList.as_view(), name='mine'),
    path('offers/', PollList.as_view(), name='offers'),
    path('buyOffer/', BuyHandler.as_view(), name='buy-offer'),
]
