from django import forms
from .models import AlgorithmModel

class AlgorithmForm(forms.ModelForm):
    class Meta:
        model = AlgorithmModel
        fields = ('option',)
        widgets = {
            'option' : forms.RadioSelect
        }