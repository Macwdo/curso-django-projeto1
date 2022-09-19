from django.shortcuts import render, get_list_or_404, get_object_or_404
from recipes.models import Recipe
from django.db.models import Q
from django.http import Http404
from django.views.generic import ListView


from utils.pagination import make_pagination
# Create your views here.

import os

PER_PAGE = os.environ.get('PER_PAGE', 6)


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/pages/home.html'
    context_object_name = 'recipes'
    ordering = ['-id']
    
    def get_queryset(self,*args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True
        )
        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )
        ctx.update({
            'recipes':page_obj,
            'pagination_range': pagination_range
            })
        
        
        return ctx

class RecipeListViewHome(RecipeListView):
    template_name = 'recipes/pages/home.html'

class RecipeListViewCaregory(RecipeListView):
    template_name = 'recipes/pages/home.html'
    

    


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_object, pagination_range = make_pagination(request, recipes, PER_PAGE)
    return render(request, 'recipes/pages/home.html', context={
        'recipes_context': recipes,
        'recipes': page_object,
        'pagination_range': pagination_range
    })  # noqa: E501


def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id'), category__id=category_id, is_published=True)  # noqa: E501
    page_object, pagination_range = make_pagination(request, recipes, PER_PAGE)  # noqa: E501

    return render(request, 'recipes/pages/category.html', context={
        'category_context': recipes,
        'recipes': page_object,
        'pagination_range': pagination_range,
        'title': f'{recipes[0].category.name}'
        })  # noqa: E501


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(request, 'recipes/pages/recipes-view.html', context={'recipe': recipe, "is_detail_page": True})  # noqa: E501


def search(request):

    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(Q(Q(title__icontains=search_term) | Q(description__icontains=search_term)), is_published=True).order_by('-id')  # noqa: E501

    page_object, pagination_range = make_pagination(request, recipes, PER_PAGE)
    return render(request, 'recipes/pages/search.html', {
        'page_title': f"Search for {search_term}",
        'search_term': search_term,
        'recipes': page_object,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}'
    })
