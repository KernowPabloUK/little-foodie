from django import forms
from datetime import date
from .models import Child


class AddChildForm(forms.ModelForm):
    """
    Form for adding a new child to a user's profile.

    This form collects the child's name and birthdate, ensures the birthdate
    is not in the future, and uses a date input widget for user-friendly
    date selection.
    """
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
        """
        Meta class to specify the model and fields used by the form.
        """
        model = Child
        fields = ('name', 'birthdate',)

    def clean_birthdate(self):
        """
        Validate that the birthdate is not in the future.

        Returns:
            date: The validated birthdate.

        Raises:
            forms.ValidationError: If the birthdate is in the future.
        """
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate and birthdate > date.today():
            raise forms.ValidationError('Birth date cannot be in the future.')
        return birthdate
