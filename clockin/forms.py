from django import forms

from .models import IntervalWork

class ClockinForm(forms.ModelForm):

    class Meta:
        model = IntervalWork
        fields = ('finished',)
