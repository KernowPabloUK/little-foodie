from django import forms
from django.utils import timezone
from .models import (
    FoodLog,
    CONSISTENCY,
    PREPARATION,
    FEED_METHOD,
    SATISFACTION,
)
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
        queryset=Food.objects.all().order_by('name'),
        empty_label="Select a food...",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'food-select'
        })
    )

    consistency = forms.ChoiceField(
        choices=[('', 'Select consistency...')] + list(CONSISTENCY),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    preparation = forms.ChoiceField(
        choices=[('', 'Select preparation...')] + list(PREPARATION),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    feeding_method = forms.ChoiceField(
        choices=[('', 'Select feeding method...')] + list(FEED_METHOD),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    satisfaction_level = forms.ChoiceField(
        choices=SATISFACTION,
        widget=forms.HiddenInput(),
        required=True
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
        widget=forms.HiddenInput()
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
        fields = ['food', 'volume', 'favourite', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_time = timezone.now().strftime('%Y-%m-%dT%H:%M')
        self.fields['log_datetime'].initial = initial_time


class CreateFoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'category', 'min_age_months', 'is_allergen']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'newFoodName'}),
            'category': forms.Select(attrs={'class': 'form-select', 'id': 'newFoodCategory'}, choices=[
                ('', 'Select a category'),
                (0, 'Fruit'),
                (1, 'Vegetable'),
                (2, 'Starch'),
                (3, 'Dairy'),
                (4, 'Protein'),
            ]),
            'min_age_months': forms.NumberInput(attrs={'class': 'form-control', 'id': 'newFoodMinAge', 'min': 0, 'max': 24}),
            'is_allergen': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'newFoodAllergen'}),
        }
        labels = {
            'name': 'Food Name',
            'category': 'Category',
            'min_age_months': 'Minimum Age (months)',
            'is_allergen': 'Contains common allergens',
        }
