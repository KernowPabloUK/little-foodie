from django import forms
from datetime import date
from .models import Child


class AddChildForm(forms.ModelForm):
    birthdate = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'max': date.today().strftime('%Y-%m-%d')
            }
        ),
        required=True
    )

    class Meta:
        model = Child
        fields = ('name', 'birthdate',)

    def clean_birthdate(self):
        """Form-level validation for birthdate"""
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate and birthdate > date.today():
            raise forms.ValidationError('Birth date cannot be in the future.')
        return birthdate
