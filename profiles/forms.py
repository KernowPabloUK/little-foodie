from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'birth_date',)
        widgets = {
            'birth_date': forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'dd-mm-yyyy'}),
        }
        input_formats = {
            'birth_date': ['%d-%m-%Y'],
        }
