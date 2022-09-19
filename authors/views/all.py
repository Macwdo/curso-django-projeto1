from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from authors.forms import RegisterForm, LoginForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe
from authors.forms.recipe_form import AuthorRecipeForm


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create')
    })


def register_create(request):
    if not request.POST:
        raise Http404()
    request.session['register_form_data'] = request.POST
    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is created, please log in.')
        del(request.session['register_form_data'])
        return redirect('authors:login')
    else:
        return redirect('authors:register')

          
def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', context={
        'form': form,
        'form_action': reverse('authors:login_create')
        })


def login_create(request):
    if not request.POST:
        raise Http404()
    form = LoginForm(request.POST)
    login_url = reverse('authors:login')
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', '')
        )
        if authenticated_user is not None:
            messages.success(request, 'You are logged in')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Error to validate form data')
        
    return redirect(reverse('authors:dashboard'))
          
            
@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect(reverse('authors:login'))
    
    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))
    
    logout(request)
    url = reverse('authors:login')
    return redirect(url)    
    
    
@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published = False,
        author = request.user
    )
    return render(request,"authors/pages/dashboard.html",context={'recipes': recipes})


@login_required(login_url='authors:login', redirect_field_name='next')
def dashoboard_recipe_create(request):
    form = AuthorRecipeForm(
        request.POST or None,
        files= request.FILES or None,
        )
    return render(request,'authors/pages/dashboard_create.html',context={
        'form':form,
        'form_action':reverse('authors:dashboard_recipe_create_post')
        
        })


def dashboard_recipe_create_post(request):
    if not request.POST:
        raise Http404
    else:
        form = AuthorRecipeForm(
        request.POST or None,
        files= request.FILES or None,
        )
        
        if form.is_valid():
            recipe = Recipe.objects.create(
                is_published = False,
                author = request.user,
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                preparation_time=request.POST.get('preparation_time'),
                preparation_time_unit=request.POST.get('preparation_time_unit'),
                servings=request.POST.get('servings'),
                servings_unit=request.POST.get('servings_unit'),
                preparation_steps=request.POST.get('preparation_steps'),
                cover=request.POST.get('cover'),
                slug=str(request.POST.get('title')) + 'slug'
        )
            messages.success(request,'Sua receita foi Criada com sucesso')
            return redirect(reverse('authors:dashboard'))

    
def dashboard_recipe_edit(request,id):
    recipe = Recipe.objects.filter(
        is_published = False,
        author = request.user,
        pk=id
    ).first()
    if not recipe:
        raise Http404
    
    form = AuthorRecipeForm(
        request.POST or None,
        files= request.FILES or None,
        instance=recipe
    )
    
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.save()
        
        messages.success(request,'Sua receita foi salva com sucesso')
        return redirect(reverse('authors:dashboard_recipe_edit',kwargs={'id':id}))
    
    return render(request, "authors/pages/dashboard_recipe.html",context={'form': form})

def dashboard_recipe_delete(request,id):
    if request.method != "POST":
        raise Http404
    recipe = Recipe.objects.filter(id=id,is_published=False,author=request.user).first()
    if not recipe:
        raise Http404
    recipe.delete()
    messages.success(request,'Deleted Successfully')
    return redirect(reverse('authors:dashboard'))