from django.urls import path
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('search/', views.search, name="search"),
    path('<int:id>/', views.recipe, name="recipe"),
    path('category/<int:category_id>/', views.category, name="category"),
]