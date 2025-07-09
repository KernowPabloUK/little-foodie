from django import forms
from .models import Child


class AddChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ('user', 'name', 'birthdate',)
