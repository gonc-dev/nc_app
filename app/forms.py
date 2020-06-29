from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Customer

class CustomerCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email')

class CustomerChangeForm(UserChangeForm):

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name','username', 'email', 'address_line_1', 'address_line_2', 'cell_number', 'telephone_number',  'city')


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)