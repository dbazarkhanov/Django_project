from django.forms import model_to_dict
from django.http import JsonResponse
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


class CurrencyList(APIView):
    def get(self, request):
        coins_data = CMC(API_KEY).getAllCoins()
        currencies = []

        for coin in coins_data:
            currency, created = Currency.objects.update_or_create(
                symbol=coin['symbol'],
                defaults={
                    'id': coin['id'],
                    'cmc_rank': coin['cmc_rank'],
                    'name': coin['name'],
                    'price': coin['quote']['USD']['price'],
                    'percent_change_24h': coin['quote']['USD']['percent_change_24h'],
                    'percent_change_7d': coin['quote']['USD']['percent_change_7d'],
                    'volume_24h': coin['quote']['USD']['volume_24h'],
                    'market_cap': coin['quote']['USD']['market_cap'],
                }
            )
        
            currencies.append(currency)
        
        serializer = CurrencySerializer(currencies, many=True)

        return JsonResponse(serializer.data, safe=False)


class CurrencyView(APIView):
    def get(self, request):
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        return render(request, 'crypt.html', {'currencies': serializer.data})


class CurrencyDetail(generics.RetrieveAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

    def get(self, request, id):
        currency = Currency.objects.get(id=id)
        serializer = CurrencySerializer(currency)  
        coin_meta_data = CMC(API_KEY).getCoinMetadata(currency.id)

        if coin_meta_data['description'] not in currency.description:
            currency.image = coin_meta_data['logo']
            currency.description = coin_meta_data['description']
            currency.save()
            
        return render(request, 'b_details.html', {'currency': serializer.data})
    

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