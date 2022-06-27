from django.shortcuts import render
# Create your views here.


def home(request):
    return render(request, 'recipes/pages/home.html', context={'nome': 'Macedo'})


def recipe(request, id):
    return render(request, 'recipes/pages/recipes-view.html', context={'nome': 'Macedo'})