from django.shortcuts import redirect, render
from authors.forms import RegisterForm
from django.http import Http404
# Create your views here.


def register_view(request):
    register_form_data = request.session.get('register_form_data',None)
    form = RegisterForm()
    return render(request, 'authors/pages/register_view.html', context={'form': form})  # noqa: E501


def register_create(request):

    if not request.POST:
        raise Http404()
    
    POST = request.POST
    request.session['register_for_data'] = POST
    form = RegisterForm(POST)

    
    return redirect('authors:register')
