from django import forms
from .models import JoinRequest


class JoinForm(forms.ModelForm):
    class Meta:
        model = JoinRequest
        fields = ['club', 'name', 'email', 'message']
        widgets = {
            'club': forms.Select(attrs={'class': 'input'}),
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'you@strathmore.edu'}),
            'message': forms.Textarea(attrs={'class': 'input', 'rows': 4, 'placeholder': 'Why do you want to join? (optional)'}),
        }