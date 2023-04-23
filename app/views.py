from django.shortcuts import render
from .models import Poll

# Create your views here.

def index(request):
    context = {
        'title': 'app',
        'polls': Poll.objects.all(),
    }
    return render(request, 'app/index.html', context)