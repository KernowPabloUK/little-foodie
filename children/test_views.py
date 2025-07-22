from django.test import TestCase
from django.urls import reverse
from testhelper.utils import create_test_user_and_child, TEST_DATA
from children.models import Child
from children.forms import AddChildForm
from datetime import date


class TestChildrenViews(TestCase):
    """
    Test suite for the children app views.

    This class contains tests for adding a child and confirming deletion
    of a child, ensuring that the correct templates are rendered,
    forms are present, and database changes occur as expected.
    """

    def setUp(self):
        """
        Set up a test user, profile, and child, and log in the test client.
        """
        self.user, self.profile, self.child = create_test_user_and_child()
        self.client.login(
            username=TEST_DATA["USERNAME"],
            password=TEST_DATA["PASSWORD"]
        )

    def test_add_child_get(self):
        """
        Test GET request to add_child view.

        Ensures the correct template is used and the AddChildForm
        is present in the context.
        """
        response = self.client.get(reverse('add_child'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'children/add_child.html')
        self.assertIsInstance(
            response.context['add_child_form'],
            AddChildForm
        )

    def test_add_child_post(self):
        """
        Test POST request to add_child view.

        Verifies that a new child is created and the user is redirected
        to the profile page.
        """
        response = self.client.post(
            reverse('add_child'),
            {
                'name': 'TestBaby',
                'birthdate': date.today()
            }
        )
        self.assertRedirects(response, reverse('profile'))
        self.assertTrue(
            Child.objects.filter(
                name='TestBaby',
                user=self.profile
            ).exists()
        )

    def test_confirm_delete_child_get(self):
        """
        Test GET request to confirm_delete_child view.

        Ensures the correct template is rendered for confirming child deletion.
        """
        url = reverse('confirm_delete_child', args=[self.child.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'children/confirm_delete_child.html')

    def test_confirm_delete_child_post(self):
        """
        Test POST request to confirm_delete_child view.

        Verifies that the child is deleted and the user is redirected
        to the profile page.
        """
        url = reverse('confirm_delete_child', args=[self.child.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('profile'))
        self.assertFalse(Child.objects.filter(id=self.child.id).exists())
