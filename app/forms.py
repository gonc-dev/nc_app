from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Customer
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (HTML,
                                 Row,
                                 Column,
                                 Fieldset,
                                 Layout,
                                 Submit)

class CustomerCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email')

class CustomerChangeForm(UserChangeForm):

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name','username', 'email', 'address_line_1', 'address_line_2', 'cell_number', 'telephone_number',  'city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='col-md-6 col-sm-12'),
                Column('last_name', css_class='col-md-6 col-sm-12')
            ),
            'username',
            'email',
            Row(
                Column('address_line_1',
                        'address_line_2',
                        'city', css_class='col-md-6 col-sm-12'),
                Column('cell_number',
                        'telephone_number', css_class='col-md-6 col-sm-12')
            ),
            
            

        )

        self.helper.add_input(Submit('submit', 'Submit'))

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)