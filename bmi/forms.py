from django import forms

class BmiForm(forms.Form):
    weight = forms.IntegerField(label="体重")
    height = forms.IntegerField(label="身長")

