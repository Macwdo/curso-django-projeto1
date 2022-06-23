from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home(request):
    return render(request, 'recipes/home.html', context={'nome':'Danilo'})


def contato(request):
    return render(request, 'recipes/temp.html',context={'numero':'993406469'})


def sobre(request):
    return HttpResponse('Sobre nós')

