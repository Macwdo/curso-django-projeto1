from django import forms
from django import http
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import Http404

class RegisterForm(forms.ModelForm):
    password = forms.CharField(required=True, widget=forms.PasswordInput({
        'placeholder': "Your password"}
    ),error_messages={
        'required': 'Password must not be empty'
    })

    first_name = forms.CharField(required=True, widget=forms.TextInput({
        'placeholder':'Ex : Danilo'
    }))

    last_name = forms.CharField(required=True, widget=forms.TextInput({
        'placeholder':'Ex : Macedo'
    }))

    email = forms.CharField(required=True, widget=forms.TextInput({
        'placeholder':'Ex : xxxxx@xxxx.xxx'
    }),help_text="Insert a valid E-mail")

    password2 = forms.CharField(required=True, widget=forms.PasswordInput({
        'placeholder': "Repeat Your Password"}
    ),error_messages={
        'required': 'Password must not be empty'
    },help_text='The length shold be at least 8 characters')

    
    class Meta:
        model = User
        fields = [
        'username',
        'first_name',
       'last_name',
        'email',
        'password'
        ] 
        #Inclui os campos a serem mostrados

    #Exclude = ['first_name'] Exclui o campo q n quer ser mostrado

        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'E-mail',
            'password': 'Password',
        }

        help_texts = {
            'email': 'Insira um e-mail valido'
        } # Textos para ajuda

        error_messages = {
            'username': {
                'required': 'Este campo é obrigatório'
            }
        } # mensagens de error

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Insira seu username aqui'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder' : 'Insira sua senha aqui'
            })
        }
    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'atenção' in data:
            raise ValidationError(
                'Não digite %(value)s no campo password',
                code='invalid',
                params={'value': 'atenção'}
            )
        return data

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            return Http404()