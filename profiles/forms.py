from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    """
    Form for editing a user's profile information.

    Allows users to update their first name, last name, and birth date.
    """

    class Meta:
        """
        Meta class to specify the model and fields used by the form.
        """

        model = Profile
        fields = ('first_name', 'last_name', 'birth_date',)
