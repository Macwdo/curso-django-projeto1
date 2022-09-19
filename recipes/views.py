from django.shortcuts import render, get_list_or_404, get_object_or_404
from recipes.models import Category, Recipe
from django.db.models import Q
from django.http import Http404
from django.views.generic import ListView , DetailView


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


class RecipeListViewCategory(RecipeListView):
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,category__id=self.kwargs.get('category_id')
        )
        return qs
    

class RecipeListViewSearch(RecipeListView):
    template_name = 'recipes/pages/search.html'
    
    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(Q(
            Q(title__icontains=search_term) | Q(description__icontains=search_term)
            ),is_published=True).order_by('-id')
        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )
        ctx.update({
            'page_title': f"Search for {search_term}",
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}'
            })
        
        return ctx 

class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipes-view.html'
    
    def get_context_data(self, *args,**kwargs):
        ctx = super().get_context_data(*args,**kwargs)
        ctx.update({
            'is_detail_page': True
        })
        return ctx