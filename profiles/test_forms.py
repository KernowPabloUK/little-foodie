from django.test import TestCase
from profiles.forms import ProfileForm
from datetime import date


class TestProfileForm(TestCase):
    """Tests for the ProfileForm."""

    def test_valid_form(self):
        """ProfileForm is valid with all required fields filled"""
        form = ProfileForm(data={
            'first_name': 'Sam',
            'last_name': 'Porter',
            'birth_date': date(1990, 1, 1)
        })
        self.assertTrue(form.is_valid())

    def test_missing_first_name(self):
        """ProfileForm is valid when first_name is missing"""
        form = ProfileForm(data={
            'first_name': '',
            'last_name': 'Porter',
            'birth_date': date(1990, 1, 1)
        })
        self.assertTrue(form.is_valid())

    def test_missing_last_name(self):
        """ProfileForm is valid when last_name is missing"""
        form = ProfileForm(data={
            'first_name': 'Sam',
            'last_name': '',
            'birth_date': date(1990, 1, 1)
        })
        self.assertTrue(form.is_valid())

    def test_missing_birth_date(self):
        """ProfileForm is valid when birth_date is missing"""
        form = ProfileForm(data={
            'first_name': 'Sam',
            'last_name': 'Porter',
            'birth_date': ''
        })
        self.assertTrue(form.is_valid())
