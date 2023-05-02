from django.db import models
from django.http import JsonResponse
from requests import Session
import json
from app.secrets import API_KEY
import sys
sys.path.append('/Users/Dell/Desktop/KBTU/django/project/user')
from user .models import User
from django.db import models

# Create your models here.

class Currency(models.Model):
    name = models.CharField(null=True, max_length=100)
    symbol = models.CharField(null=True, max_length=100)
    image = models.ImageField(upload_to='media/currency/', max_length=254, default='')
    price = models.FloatField(default=0)


class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='balance')
    balance = models.FloatField(default=0)
    currency_id = models.ForeignKey(to=Currency, on_delete=models.CASCADE,)
    quantity = models.FloatField(null=True)
    image = models.ImageField(upload_to='media/', max_length=254, default='')

    def __str__(self):
        return f"{self.user}"

#Stores historical data (all transactions of all users)
class Transaction(models.Model):
    type = models.CharField(max_length=10, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user')
    to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='to')
    currency_id = models.ForeignKey(to=Currency, on_delete=models.CASCADE,)
    quantity = models.FloatField(default=0)

    def sum(self):
        return self.currency_id.price * self.quantity

class Poll(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    currency = models.ForeignKey(to=Currency, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Объявление о продаже {self.user.username}"

    def sum(self):
        return self.currency.price * self.quantity
    
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
            'limit': '25'
        }
        url = self.apiUrl + '/v1/cryptocurrency/listings/latest'
        response = self.session.get(url, params=parameters)
        data = json.loads(response.text)['data']
        return JsonResponse(data, safe=False)

    def getCoinMetadata(self, id):
        parameters = {
            'id': id
        }
        url = self.apiUrl + '/v2/cryptocurrency/info'
        response = self.session.get(url, params=parameters)
        data = json.loads(response.text)['data'][str(id)]
        return JsonResponse(data, safe=False)

    def getCoinDetails(self, id):
        parameters = {
            'id': id
        }
        url = self.apiUrl + '/v2/cryptocurrency/quotes/latest'
        response = self.session.get(url, params=parameters)
        data = json.loads(response.text)['data'][str(id)]
        return JsonResponse(data, safe=False)