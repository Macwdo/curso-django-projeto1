from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import strong_password


class RegisterForm(forms.ModelForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Your username"}),
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Your password must be greater than 4 characters',
            'max_length': "Your password must be less 150 characters"},
        label="Username",
        help_text="Your username must be greater than 4 characters and less 150. Letters, numbers and @/./+/-/_ only.",
        min_length=4,
        max_length=150
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Your first name'}),
        error_messages={'required': 'Write your first name'},
        label="First name")
    
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Your last name'}),
        error_messages={'required': 'Write your last name'},
        label="Last name")
    
    email = forms.EmailField(
        widget=forms.EmailInput({'placeholder': 'Your email'}),
        error_messages={'required': 'Email is required.'},
        label='E-Mail',
        help_text='Please Insert a valid E-mail'
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=("""Password must have at least one uppercase letter, one lowercase letter and one number. The length should be at least 8 characters."""),
        validators=[strong_password],
        label='Password'
    )

    password2 = forms.CharField(
        label="Repeat your pass",
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        }),
        help_text=("This field must be equal password field")
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        labels = {
            'username': 'Username',
            'last_name': 'Last name',
            'first_name': 'First name',
            'email': 'E-Mail',
        }
        
        error_messages = {
            'username': {
                'required': 'This field must not be empty'}
        }
        
        help_texts = {
            'username': 'Mandatory. 150 characters or less. Letters, numbers and @/./+/-/_ only.'
        }

        widgets = {
            'username': forms.TextInput(attrs={
                "placeholder": "Your username"
            })
        }
        
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()
        
        if exists:
            raise ValidationError('User e-mail is already in use', code='invalid')

        return email
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise ValidationError(
                {'password2': 'Please insert equal passwords'}
            )
