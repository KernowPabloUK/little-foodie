from django.test import TestCase
from children.forms import AddChildForm
from datetime import date, timedelta
from testhelper.utils import create_test_user_and_profile, TEST_DATA


class TestChildrenForms(TestCase):
    def setUp(self):
        self.user, self.profile = create_test_user_and_profile()

    def test_valid_form(self):
        """Test AddChildForm is valid"""
        form = AddChildForm(
            data={'name': TEST_DATA["CHILD_NAME"], 'birthdate': date.today()}
        )
        self.assertTrue(form.is_valid())

    def test_name_is_required(self):
        """Test name field"""
        form = AddChildForm(
            data={'name': '', 'birthdate': date.today()}
        )
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_birthdate_is_required(self):
        """Test birthdate field"""
        form = AddChildForm(
            data={'name': TEST_DATA["CHILD_NAME"], 'birthdate': ''}
        )
        self.assertFalse(form.is_valid())
        self.assertIn('birthdate', form.errors)

    def test_future_birthdate_invalid(self):
        """Test birthdate field validity"""
        future_date = date.today() + timedelta(days=1)
        form = AddChildForm(
            data={'name': TEST_DATA["CHILD_NAME"], 'birthdate': future_date}
        )
        self.assertFalse(
            form.is_valid(), msg='Birth date cannot be in the future.'
        )

    def test_form_save_creates_child(self):
        """Test AddChildForm creates a child"""
        form = AddChildForm(
            data={'name': TEST_DATA["CHILD_NAME"], 'birthdate': date.today()}
        )
        self.assertTrue(form.is_valid())
        child = form.save(commit=False)
        child.user = self.profile
        child.save()
        self.assertEqual(child.name, TEST_DATA["CHILD_NAME"])
        self.assertEqual(child.birthdate, date.today())
        self.assertEqual(child.user, self.profile)
