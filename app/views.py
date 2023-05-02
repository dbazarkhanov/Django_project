from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics
# Create your views here.

class CurrencyList(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    
    def get(self, request):
        currencies = self.get_queryset()
        return render(request, 'currency_list.html', {'currencies': currencies})

class CurrencyDetail(generics.RetrieveAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class BalanceList(generics.ListAPIView):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer

    def get(self, request):
        balancies = self.get_queryset()
        return render(request, '.html', {'balancies': balancies})

class BalanceDetail(generics.RetrieveAPIView):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer

class TransactionList(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get(self, request):
        transactions = self.get_queryset()
        return render(request, '.html', {'transactions': transactions})

class TransactionDetail(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class PollList(generics.ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get(self, request):
        polls = self.get_queryset()
        return render(request, 'offers.html', {'polls': polls})

class PollDetail(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer