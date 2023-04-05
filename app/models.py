from django.db import models
from requests import Session
from app.secrets import API_KEY
from django.http.response import JsonResponse
import sys
sys.path.append('/Users/Dell/Desktop/KBTU/django/project/user')
from user .models import User
from django.db import models

# Create your models here.

class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='balance')
    balance = models.FloatField(default=0)
    currency_id = models.IntegerField(null=True)
    quantity = models.FloatField(null=True)
    image = models.ImageField(upload_to='media/', max_length=254, default='')

    def __str__(self):
        return f"{self.user}"

#Stores historical data (all transactions of all users)
class Transaction(models.Model):
    type = models.CharField(max_length=10, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user')
    to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='to')
    currency_id = models.IntegerField(null=True)
    quantity = models.FloatField(null=True)
    price = models.FloatField(null=True)

class Currency(models.Model):
    name = models.CharField(null=True, max_length=100)
    symbol = models.CharField(null=True, max_length=100)
    image = models.ImageField(upload_to='media/', max_length=254, default='')

