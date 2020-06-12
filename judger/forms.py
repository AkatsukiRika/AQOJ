from django import forms


class UserForm(forms.Form):
    usr = forms.CharField(label="USERNAME", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    pwd = forms.CharField(label="PASSWORD", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

