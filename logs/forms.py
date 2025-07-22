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
from foods.models import Food, FOOD_CATEGORY


class ChildSelectionForm(forms.Form):
    """
    Form for selecting which child to log food for.

    Presents a radio select of all children associated with the user's profile.
    """
    child = forms.ModelChoiceField(
        queryset=Child.objects.none(),
        widget=forms.RadioSelect,
        empty_label=None
    )

    def __init__(self, user, *args, **kwargs):
        """
        Initialize the form with the user's children as queryset.
        """
        super().__init__(*args, **kwargs)
        self.fields['child'].queryset = user.profile.children.all()


class FoodLogForm(forms.ModelForm):
    """
    Form for logging food for a child.

    Collects details about the feeding event, including food, volume,
    consistency, preparation, feeding method, satisfaction level,
    favourite status, and notes.
    """
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
        """
        Meta class to specify the model and fields used by the form.
        """
        model = FoodLog
        fields = ['food', 'volume', 'favourite', 'notes']

    def __init__(self, *args, **kwargs):
        """
        Initialize the form, setting the initial log_datetime
        and customizing food labels.
        """
        super().__init__(*args, **kwargs)
        initial_time = timezone.now().strftime('%Y-%m-%dT%H:%M')
        self.fields['log_datetime'].initial = initial_time
        self.fields['food'].label_from_instance = (
            lambda obj: (
                f"{obj.name}    "
                f"[{obj.get_category_display()}] "
                f"[{obj.min_age_months}m +]"
            )
        )


class CreateFoodForm(forms.ModelForm):
    """
    Form for creating a new food item.

    Collects the food's name, category, minimum age, and allergen status.
    Uses custom widgets and labels for user-friendly input.
    """
    class Meta:
        """
        Meta class to specify the model, fields, widgets,
        and labels used by the form.
        """
        model = Food
        fields = ['name', 'category', 'min_age_months', 'is_allergen']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'newFoodName'
                }
            ),
            'category': forms.Select(
                attrs={'class': 'form-select', 'id': 'newFoodCategory'},
                choices=[('', 'Select a category')] + list(FOOD_CATEGORY)
            ),
            'min_age_months': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'newFoodMinAge',
                    'min': 0,
                    'max': 24
                }
            ),
            'is_allergen': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'id': 'newFoodAllergen'
                }
            ),
        }
        labels = {
            'name': 'Food Name',
            'category': 'Category',
            'min_age_months': 'Minimum Age (months)',
            'is_allergen': 'Contains common allergens',
        }
