from django import forms

class NameForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField()
    password = forms.CharField(label='Password', max_length=25)
