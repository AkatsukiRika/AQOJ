<<<<<<< HEAD
from django import forms


class UserForm(forms.Form):
    usr = forms.CharField(label="USERNAME", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    pwd = forms.CharField(label="PASSWORD", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

=======
from django import forms


class UserForm(forms.Form):
    usr = forms.CharField(label="USERNAME", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    pwd = forms.CharField(label="PASSWORD", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

>>>>>>> 925150b4b2604b4b2f453c3826270df15953848c
