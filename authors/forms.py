from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
        'username',
        'first_name',
        'email',
        'last_name',
        'password'
        ] 
        #Inclui os campos a serem mostrados

    #Exclude = ['first_name'] Exclui o campo q n quer ser mostrado

        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'E-mail',
            'password': 'Password'
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