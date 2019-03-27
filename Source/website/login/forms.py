from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username:', max_length=100, widget=forms.TextInput)
    password = forms.CharField(label='Password:', max_length=100, widget=forms.PasswordInput)
