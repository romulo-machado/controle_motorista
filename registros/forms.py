from .models import RegistroGanho
from .models import Despesa
from django import forms

class RegistroGanhoForm(forms.ModelForm):
    class Meta:
        model = RegistroGanho
        fields = ['data', 'plataforma', 'corridas', 'valor_bruto', 'promocoes', 'gorjeta']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'plataforma': forms.TextInput(attrs={'class': 'form-control'}),
            'corridas': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_bruto': forms.NumberInput(attrs={'class': 'form-control'}),
            'promocoes': forms.NumberInput(attrs={'class': 'form-control'}),
            'gorjeta': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['data', 'tipo', 'descricao', 'valor']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
        }