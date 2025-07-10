from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from .models import FoodLog, Consistency, Preparation, FeedingMethod, SatisfactionLevel
from children.models import Child
from foods.models import Food


class ChildSelectionForm(forms.Form):
    """Form for selecting which child to log food for"""
    child = forms.ModelChoiceField(
        queryset=Child.objects.none(),
        widget=forms.RadioSelect,
        empty_label=None
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['child'].queryset = user.profile.children.all()


class FoodLogForm(forms.ModelForm):
    """Form for logging food for a child"""
    # Create a separate datetime field that's not tied to the model field
    log_datetime = forms.DateTimeField(
        label="Date & Time",
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        input_formats=['%Y-%m-%dT%H:%M'],
        initial=timezone.now
    )
    
    food = forms.ModelChoiceField(
        queryset=Food.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'food-select'
        })
    )
    
    consistency = forms.ModelChoiceField(
        queryset=Consistency.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    preparation = forms.ModelChoiceField(
        queryset=Preparation.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    feeding_method = forms.ModelChoiceField(
        queryset=FeedingMethod.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    satisfaction_level = forms.ModelChoiceField(
        queryset=SatisfactionLevel.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'satisfaction-radio'})
    )
    
    volume = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'placeholder': 'Number of teaspoons'
        }),
        help_text="Approximate volume in teaspoons"
    )
    
    favourite = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Additional notes about this feeding...'
        })
    )

    class Meta:
        model = FoodLog
        fields = ['food', 'consistency', 'preparation', 
                 'feeding_method', 'volume', 'satisfaction_level', 
                 'favourite', 'notes']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial datetime to current time
        self.fields['log_datetime'].initial = timezone.now().strftime('%Y-%m-%dT%H:%M')