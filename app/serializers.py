from rest_framework import serializers
from .models import Currency, Transaction, Poll
import sys
sys.path.append(r'/Users/araimbayeva/Desktop/Django/DjangoProject/user/')
from user.serializers import UserSerializer


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

'''
class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = '__all__'
'''

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class PollSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    currency = CurrencySerializer(many=False)
    class Meta:
        model = Poll
        fields = '__all__'
