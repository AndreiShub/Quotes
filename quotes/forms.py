from django import forms
from .models import Quote

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'source']
        labels = {
            'text': '',
            'source': '',
        }
        widgets = {
            'text': forms.TextInput(attrs={'class': 'quote-input', 'placeholder': 'Текст цитаты'}),
            'source': forms.TextInput(attrs={'class': 'quote-input', 'placeholder': 'Источник'}),
        }
