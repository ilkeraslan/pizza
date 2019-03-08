from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        error_messages={'required': 'Please enter your username.'},
        help_text='Username',
        label='Username',
        max_length=100,
    )
    email = forms.EmailField(
        error_messages={
            'required': 'Please enter your email.',
            'invalid': 'Enter a valid email address.'
        },
        help_text='Email',
    )
    password = forms.CharField(
        error_messages={'required': 'Please enter your password.'},
        label='Password',
        max_length=25,
        widget=forms.PasswordInput,
    )


class SignupForm(UserCreationForm):
    first_name = forms.CharField(
        label='First Name',
        max_length=30,
        required=False
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=30,
        required=False
    )
    email = forms.EmailField(
        label='Email',
        max_length=100,
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
