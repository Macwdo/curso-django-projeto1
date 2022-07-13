import http
from django.shortcuts import render, get_list_or_404, get_object_or_404
from recipes.models import Recipe
from django.http import Http404
# Create your views here.


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={'recipes': recipes})  # noqa: E501


def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id'), category__id=category_id, is_published=True)  # noqa: E501
    
    return render(request, 'recipes/pages/category.html', context={'recipes': recipes, 'title': f'{recipes[0].category.name}'})  # noqa: E501


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(request, 'recipes/pages/recipes-view.html', context={'recipe': recipe, "is_detail_page": True})  # noqa: E501


def search(request):
    search_term = request.GET.get('q')

    if not search_term:
        raise Http404()
    
    return render(request, 'recipes/pages/search.html')
