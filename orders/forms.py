from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class CustomLoginForm(AuthenticationForm):

    username = forms.CharField(
        label='Username',
        max_length=30,
        required=True,
    )

    email = forms.EmailField(
        help_text='Email',
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput()
    )

    def clean(self):
        cleaned_data = super(CustomLoginForm, self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if not username:
            raise forms.ValidationError('Please provide your unique username.')
        if not password:
            raise forms.ValidationError('Provide your password.')
        if not email:
            raise forms.ValidationError('Please provide your email.')


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
    birth_date = forms.DateField(
        help_text='Required. Format: YYYY-MM-DD',
        label='Birth Date',
        required=True,
    )

    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'birth_date', 'email', 'password1', 'password2',)
