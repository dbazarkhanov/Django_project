from rest_framework import serializers
from .models import Currency, Transaction, Poll
import sys
sys.path.append('/Users/Dell/Desktop/KBTU/django/project/user')
from user.serializers import UserSerializer


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class PollSerializer(serializers.ModelSerializer):
    #user = serializers.PrimaryKeyRelatedField(read_only=True)
    #currency = serializers.PrimaryKeyRelatedField(read_only=True)
    currency = CurrencySerializer()
    class Meta:
        model = Poll
        fields = '__all__'

