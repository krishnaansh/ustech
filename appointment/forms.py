from django import forms
from django.forms import ModelForm
from django.db import models
from appointment.models import *
from django.core import validators
from django.contrib.auth.models import User
from django.core.validators import *
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError


FIELD_NAME_MAPPING = {
    'username': 'uname',    
}
class LoginForm(forms.Form):    
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id' : "inputEmail" ,
                    'placeholder' : 'Enter Email or Username', 'autofocus' : 'autofocus'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id' : "inputPassword" ,
                     'placeholder' : 'Enter Password', 'autofocus' : 'autofocus'}),validators=[validators.MinLengthValidator(5)])
  

class regForm(forms.Form):    
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id' : "firstName" ,
                    'placeholder' : 'Enter Name', 'autofocus' : 'autofocus'}),validators=[validators.MinLengthValidator(5), validators.MaxLengthValidator(10)])
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id' : "inputEmail" ,
                    'placeholder' : 'Enter Email'}),validators=[validators.validate_email])

    uname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id' : "username" ,
                    'placeholder' : 'Enter Username'}),validators=[validators.MinLengthValidator(5), validators.MaxLengthValidator(8)])
                    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id' : "inputPassword" ,
                     'placeholder' : 'Enter Password'}),validators=[validators.MinLengthValidator(5), validators.MaxLengthValidator(8)])

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('email')
        uname = cleaned_data.get('uname')

        if User.objects.filter(email=email).exists() == True and User.objects.filter(email=email).exists() == True:            
            # self._errors['email'] 
            raise forms.ValidationError({'email': ["Email is already exist",], 'uname': ["Username is already exist",]})
        
        if User.objects.filter(email=email).exists() == True:            
            # self._errors['email'] 
            raise forms.ValidationError({'email': ["Email is already exist",]})

        if User.objects.filter(username=uname).exists() == True:            
            # self._errors['email'] 
            raise forms.ValidationError({'uname': ["Username is already exist",]})

        return self.cleaned_data
