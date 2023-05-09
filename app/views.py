from http.client import HTTPResponse
from urllib import response
from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
import math
import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')


# Create your views here.

class CurrencyList(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    
    # def get(self, request):
    #     currencies = self.get_queryset()
    #     return render(request, 'currency_list.html', {'currencies': currencies})

class CurrencyDetail(generics.RetrieveAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

    def get(self, request):
        currency_details = self.get_queryset()
        return render(request, 'currency_list.html', {'currencies': currency_details})

'''
class BalanceList(generics.ListAPIView):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer

    def get(self, request):
        balancies = self.get_queryset()
        return render(request, 'currency_list.html', {'balancies': balancies})

class BalanceDetail(generics.RetrieveAPIView):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
'''

class TransactionList(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get(self, request):
        transactions = self.get_queryset()
        return render(request, 'currency_list.html', {'transactions': transactions})

class TransactionDetail(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class BuyHandler(APIView):
    def post(self, request):
        data = request.data
        pollId = data.get("pollId")
        quantity = float(data.get("quantity"))
        buyer = request.user

        try:
            poll = Poll.objects.get(id=pollId)
        except Poll.DoesNotExist:
            poll = None

        if poll is None:
            return Response({"message": "Poll not found"})
        if quantity < 0 or math.isclose(quantity, 0):
            return Response({"message": "Quantity is less or equal zero"})

        seller = poll.user

        if(math.isclose(quantity, poll.quantity) or quantity < poll.quantity):
            buyerBalance = buyer.balance
            sumToPay = (float(poll.price) * (float(data.get("quantity"))))

            if (buyerBalance >= sumToPay):
                #Updating balance table
                buyer.balance -= sumToPay
                buyer.save()

                seller.balance += sumToPay
                seller.save()

                #Updating Polls and buyer's wallet
                pollToUpdate = Poll.objects.get(id=poll.id)
                buyerWalletElementToUpdate = list(WalletElement.objects.filter(user=buyer, currency=poll.currency))

                if(math.isclose(quantity, poll.quantity)):
                    pollToUpdate.delete()
                else:
                    pollToUpdate.quantity -= quantity
                    pollToUpdate.save()

                if (buyerWalletElementToUpdate != []):  
                    buyerWalletElementToUpdate[0].quantity += float(quantity)
                    buyerWalletElementToUpdate[0].save()
                else:
                    buyerWalletElementToCreate = \
                        WalletElement.objects.create(
                            currency=poll.currency,
                            user=buyer,
                            quantity=quantity
                        )   
                         
                newTransaction = \
                    Transaction.objects.create(
                        seller=seller,
                        buyer=buyer,
                        currency=poll.currency,
                        quantity=quantity,
                        price=sumToPay
                        )
            else:
                return Response({"message": "Not enough balance",
                                 "balance": buyerBalance})

        else:
            return Response({"message": "You are trying to buy more currency than available"})

        return Response({"message": "Success"})

    def delete(self, request):
        data = request.data
        user = request.user
        poll = data["poll"]
        serializer = PollSerializer(data=data)
        
        if serializer.is_valid():
            pollToDelete = Poll.objects.get(id=poll.id)
            pollToDelete.delete()

            WalletElementToReturn = list(WalletElement.objects.filter(user=user, currency=poll.currency))
            if (WalletElementToReturn != []):  
                WalletElementToReturn[0].quantity += float(data.get("quantity"))
                WalletElementToReturn[0].save()
            else:
                buyerWalletElementToCreate = \
                    WalletElement.objects.create(
                        currency=poll.currency,
                        user=user,
                        quantity=data.get("quantity")
                    ) 
            serializer.save()
            return Response({"message": "Success"})

        return Response(serializer.errors)

class SellHandler(APIView):
    # в дате должно быть quantity, wallet element, price
    def post(self, request):
        data = request.data
        user = request.user
        serializer = TransactionSerializer(data=data)

        if serializer.is_valid():
            quantityToSell = data.get("quantity")
            price = data.get("price")
            walletElement = data.get("walletElement")

            if(quantityToSell < walletElement.quantity or math.isclose(quantityToSell, walletElement.quantity)):
                pollToCreate = \
                    Poll.objects.create(
                        user=user,
                        currency=walletElement.currency,
                        quantity=quantityToSell,
                        price=price,
                        created_timestamp = datetime.datetime.now()
                        )

                if(math.isclose(quantityToSell, walletElement.quantity)):
                    walletElement.delete()

                else:
                    walletElement.quantity -= quantityToSell
                    walletElement.save()

                serializer.save()
                return Response({"message": "Success"})

            else:
                return Response({"message": "You are trying to sell more currency than you own"})

        return Response(serializer.errors)


class PollList(generics.ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get(self, request):
        polls = self.get_queryset()
        serializer = PollSerializer(polls, many=True)
        return render(request, 'offers.html', {'polls': serializer.data})


class PollDetail(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer