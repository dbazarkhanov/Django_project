from django.db import models
from django.http import JsonResponse
from requests import Session
import json
from app.secrets import API_KEY
import sys
sys.path.append('C:/Users/d_baz/Desktop/KBTU/django/project/user/')
from user.models import User
from django.db import models
# Create your models here.

class Currency(models.Model):
    cmc_rank = models.BigIntegerField(null=True)
    name = models.CharField(null=True, max_length=100)
    symbol = models.CharField(null=True, max_length=100)

    image = models.ImageField(upload_to='currency', max_length=254, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    percent_change_24h = models.FloatField(max_length=10, null=True)
    percent_change_7d = models.FloatField(max_length=10, null=True)
    volume_24h = models.FloatField(max_length=10, null=True)
    market_cap = models.FloatField(max_length=10, null=True)

    description = models.TextField(blank=True)

#A single element inside person's wallet
class WalletElement(models.Model):
    currency = models.ForeignKey(to=Currency, on_delete=models.CASCADE,)
    quantity = models.FloatField(null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,)

    def __str__(self):
        return f"Элемент кошелька {self.user.username}, валюта {self.currency.name}"


#Stores historical data (all transactions of all users)
class Transaction(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='to')
    currency = models.ForeignKey(to=Currency, on_delete=models.CASCADE,)
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=0)

    def sum(self):
        return self.price * self.quantity

class Poll(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    currency = models.ForeignKey(to=Currency, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Объявление о продаже {self.user.username}"

    def sum(self):
        return self.price * self.quantity
    
class CMC(models.Model):
    def __init__(self, token):
        self.apiUrl = 'https://pro-api.coinmarketcap.com'
        self.headers = {
              'Accepts': 'application/json',
              'X-CMC_PRO_API_KEY': token,
            }
        self.session = Session()
        self.session.headers.update(self.headers)

    def getAllCoins(self):
        parameters = {
            'start': '1',
            'limit': '25',
        }
        url = self.apiUrl + '/v1/cryptocurrency/listings/latest'
        response = self.session.get(url, params=parameters)

        try:
            data = json.loads(response.text)['data']
            return data
        except KeyError: 
            return 'Error'

    def getCoinMetadata(self, id):
        parameters = {
            'id': id
        }
        url = self.apiUrl + '/v2/cryptocurrency/info'
        response = self.session.get(url, params=parameters)
        try:
            data = json.loads(response.text)['data'][str(id)]
            return data
        except KeyError: 
                return 'Loading' 

    def getCoinDetails(self, id):
        parameters = {
            'id': id
        }
        url = self.apiUrl + '/v2/cryptocurrency/quotes/latest'
        response = self.session.get(url, params=parameters)

        data = json.loads(response.text)['data'][str(id)]
        return data
