from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=65)

class Recipe(models.Model):
    #Title Description Slug
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField()
    #Preparation_time preparation_time_unit
    preparation = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    #servings servings_unit
    servings = models.IntegerField()
    servings_time_unit = models.CharField(max_length=65)
    #preparation steps
    preparation_steps = models.TextField()
    #preparation steps is html
    preparation_steps_is_html = models.BooleanField(default=False)
    #created_at
    created_at = models.DateTimeField(auto_now_add=True)
    #Updated_at
    updated_at = models.DateTimeField(auto_now=True)
    #is_published
    is_published = models.BooleanField(default=False)
    #cover
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d')
    #category(relação)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
        )
    #author(relação)
    author = models.ForeignKey(
        User , on_delete=models.SET_NULL, null=True
        )

# Create your models here.
