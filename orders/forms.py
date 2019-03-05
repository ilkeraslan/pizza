from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=100,
        error_messages={'required': 'Please enter your username.'}
    )
    email = forms.EmailField(
        error_messages={
            'required': 'Please enter your email.',
            'invalid': 'Enter a valid email address.'
        }
    )
    password = forms.CharField(
        label='Password',
        max_length=25,
        widget=forms.PasswordInput,
        error_messages={'required': 'Please enter your password.'}
    )
