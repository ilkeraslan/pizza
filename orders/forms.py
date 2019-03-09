from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox, ReCaptchaV3
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class CustomLoginForm(AuthenticationForm):
    email = forms.EmailField(
        error_messages={
            'required': 'Please enter your email.',
            'invalid': 'Enter a valid email address.'
        },
        help_text='Email',
    )
    captcha = ReCaptchaField(widget=ReCaptchaV3)


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
