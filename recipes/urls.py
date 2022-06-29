from django.urls import path
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('<int:id>/', views.recipe, name="recipe"),
    path('recipes/', views.home, name='home')
    ]