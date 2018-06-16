from django import forms

class PayForm(forms.Form):

    pay_rate = forms.DecimalField(max_digits=5, decimal_places=2)
    tax = forms.DecimalField(max_digits=4, decimal_places=2)