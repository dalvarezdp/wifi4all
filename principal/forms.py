#encoding:utf-8
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User


class UserForm(forms.Form):
    class Meta:
        username = forms.CharField(label='Usuario', max_length=100)
        password1 = forms.CharField(label='Contrasena', max_length=100)
        password2 = forms.CharField(label='Repite contrasena', max_length=100)
        first_name = forms.CharField(label='Nombre', max_length=100)
        last_name = forms.CharField(label='Apellidos', max_length=100)
        email = forms.EmailField(label='Email')
        telefono = forms.NumberInput()
        
    def clean_clave(self):
        cleaned_data = super(UserForm, self).clean()
        clave = cleaned_data.get('password1')
        clave2 = cleaned_data.get('password2')
        self.add_error('password1','Las contrasenas son diferentes')
        if clave != clave2: 
            self.add_error('password1','Las contrasenas son diferentes')

     

