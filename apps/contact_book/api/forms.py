from django import forms

class BusinessCardOcrForm(forms.Form):
    image = forms.ImageField()
