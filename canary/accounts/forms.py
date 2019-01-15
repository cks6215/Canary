from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, label="UNIST Email")
    password1 = forms.CharField(widget=forms.PasswordInput, label="password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="password (again)")


class AuthenticationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, label="UNIST Email")
    password = forms.CharField(widget=forms.PasswordInput, label="password")