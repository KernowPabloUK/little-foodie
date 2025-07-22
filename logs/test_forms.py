from django.test import TestCase
from django.utils import timezone
from logs.forms import FoodLogForm, CreateFoodForm
from testhelper.utils import create_test_user_and_child, create_test_food
from foods.models import FOOD_CATEGORY


class TestLogsForms(TestCase):
    def setUp(self):
        self.user, self.profile, self.child = create_test_user_and_child()
        self.food = create_test_food(user=self.user)
        self.food_data = {
            'name': 'Apple',
            'category': 0,
            'min_age_months': 6,
            'is_allergen': False,
        }

    def test_create_food_form_valid(self):
        """CreateFoodForm is valid with all required fields."""
        form = CreateFoodForm(data=self.food_data)
        self.assertTrue(form.is_valid())

    def test_create_food_form_missing_name(self):
        """CreateFoodForm is invalid if name is missing."""
        data = self.food_data.copy()
        data['name'] = ''
        form = CreateFoodForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_create_food_form_category_choices(self):
        """CreateFoodForm category field has correct choices."""
        form = CreateFoodForm()
        choices = form.fields['category'].choices
        self.assertEqual(choices[0], FOOD_CATEGORY[0])
        for cat in FOOD_CATEGORY:
            self.assertIn(cat, choices)

    def test_create_food_form_labels(self):
        """CreateFoodForm uses custom labels."""
        form = CreateFoodForm()
        self.assertEqual(form.fields['name'].label, 'Food Name')
        self.assertEqual(form.fields['category'].label, 'Category')
        self.assertEqual(form.fields['min_age_months'].label, 'Minimum Age (months)')
        self.assertEqual(form.fields['is_allergen'].label, 'Contains common allergens')

    def test_create_food_form_invalid_category(self):
        """CreateFoodForm is invalid if category is not in FOOD_CATEGORY."""
        data = self.food_data.copy()
        data['category'] = 999 
        form = CreateFoodForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)

    def test_create_food_form_widget_types(self):
        """CreateFoodForm uses correct widget types."""
        form = CreateFoodForm()
        self.assertEqual(form.fields['name'].widget.__class__.__name__, 'TextInput')
        self.assertEqual(form.fields['category'].widget.__class__.__name__, 'Select')
        self.assertEqual(form.fields['min_age_months'].widget.__class__.__name__, 'NumberInput')
        self.assertEqual(form.fields['is_allergen'].widget.__class__.__name__, 'CheckboxInput')

    def test_food_log_form_notes_optional(self):
        """FoodLogForm is valid if notes is omitted (if notes is optional)."""
        form = FoodLogForm(data={
            'food': self.food.id,
            'volume': 2,
            'favourite': True,
            'log_datetime': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'consistency': 1,
            'preparation': 1,
            'feeding_method': 1,
            'satisfaction_level': 1,
        })
        self.assertTrue(form.is_valid())

    def test_form_valid_data(self):
        """FoodLogForm is valid with all required fields filled."""
        form = FoodLogForm(data={
            'food': self.food.id,
            'volume': 2,
            'favourite': True,
            'notes': 'Test note',
            'log_datetime': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'consistency': 1,
            'preparation': 1,
            'feeding_method': 1,
            'satisfaction_level': 1,
        })
        self.assertTrue(form.is_valid())

    def test_form_missing_required_fields(self):
        """FoodLogForm is invalid if required fields are missing."""
        form = FoodLogForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('food', form.errors)
        self.assertIn('volume', form.errors)

    def test_log_datetime_initial_format(self):
        """FoodLogForm sets log_datetime initial value in correct format."""
        form = FoodLogForm()
        initial = form.fields['log_datetime'].initial
        # YYYY-MM-DDTHH:MM format
        self.assertRegex(initial, r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}')

    def test_food_label_from_instance(self):
        """FoodLogForm food field uses custom label_from_instance."""
        form = FoodLogForm()
        label = form.fields['food'].label_from_instance(self.food)
        self.assertIn(self.food.name, label)
        self.assertIn(str(self.food.min_age_months), label)
