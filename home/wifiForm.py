
from django import forms

class WifiForm(forms.Form):
    ssid = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
