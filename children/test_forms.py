from django.test import TestCase
from children.forms import AddChildForm
from datetime import date, timedelta
from testhelper.utils import create_test_user_and_profile, TEST_DATA


class TestChildrenForms(TestCase):
    """
    Test suite for the AddChildForm in the children app.

    This class contains tests to ensure the AddChildForm validates
    input correctly, enforces required fields, prevents future birthdates,
    and properly saves a child instance.
    """

    def setUp(self):
        """
        Set up a test user and profile for use in form tests.
        """
        self.user, self.profile = create_test_user_and_profile()

    def test_valid_form(self):
        """
        Test that AddChildForm is valid with correct data.
        """
        form = AddChildForm(
            data={'name': TEST_DATA["CHILD_NAME"], 'birthdate': date.today()}
        )
        self.assertTrue(form.is_valid())

    def test_name_is_required(self):
        """
        Test that the name field is required.
        """
        form = AddChildForm(
            data={'name': '', 'birthdate': date.today()}
        )
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_birthdate_is_required(self):
        """
        Test that the birthdate field is required.
        """
        form = AddChildForm(
            data={'name': TEST_DATA["CHILD_NAME"], 'birthdate': ''}
        )
        self.assertFalse(form.is_valid())
        self.assertIn('birthdate', form.errors)

    def test_future_birthdate_invalid(self):
        """
        Test that a future birthdate is considered invalid.
        """
        future_date = date.today() + timedelta(days=1)
        form = AddChildForm(
            data={'name': TEST_DATA["CHILD_NAME"], 'birthdate': future_date}
        )
        self.assertFalse(
            form.is_valid(), msg='Birth date cannot be in the future.'
        )

    def test_form_save_creates_child(self):
        """
        Test that AddChildForm creates and saves a child instance correctly.
        """
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
