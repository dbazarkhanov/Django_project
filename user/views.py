from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm
# from rest_framework import generics
from .models import User
import sys
sys.path.append(r'/Users/araimbayeva/Desktop/Django/DjangoProject/app/')
from app.models import WalletElement


def register(request):
    if request.method == 'POST':
        data = request.POST
        form = UserRegisterForm(data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user:login'))
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'register.html', context)


def login(request):
    if request.method == 'POST':
        data = request.POST
        form = UserLoginForm(request, data)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('app:crypt'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'login.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        user = request.user
        userInfo = User.objects.get(id=user.id)
        investments = WalletElement.objects.filter(user=user)
        investments_sum = 0

        for i in investments:
            investments_sum += i.sum()
        investments_sum = round(investments_sum, 3)

        form = UserProfileForm(instance=request.user)

    context = {'form': form, 'userInfo': userInfo, 'investments': investments, 'sum': investments_sum}
    return render(request, 'profile.html', context)

# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer