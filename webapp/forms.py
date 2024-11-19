from django import forms

class UserInfoForm(forms.Form):
    name = forms.CharField(label='Nom', max_length=100)
    address = forms.CharField(label='Adresse', widget=forms.Textarea)