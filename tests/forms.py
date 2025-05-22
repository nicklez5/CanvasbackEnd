from django import forms
from .models import Tests
class TestForm(forms.ModelForm):
    class Meta:
        model = Tests
        fields = ('description','file')