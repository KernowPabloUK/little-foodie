from django.test import TestCase
from django.urls import reverse
from testhelper.utils import create_test_user_and_profile, TEST_DATA
from children.models import Child
from children.forms import AddChildForm
from datetime import date


class TestChildrenViews(TestCase):
    def setUp(self):
        self.user, self.profile = create_test_user_and_profile()
        self.client.login(
            username=TEST_DATA["USERNAME"],
            password=TEST_DATA["PASSWORD"]
        )

    def test_add_child_get(self):
        """Test GET request to add_child view
        returns correct template and form."""
        response = self.client.get(reverse('add_child'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'children/add_child.html')
        self.assertIsInstance(
            response.context['add_child_form'],
            AddChildForm
        )

    def test_add_child_post(self):
        """Test POST request to add_child view
        creates a child and redirects to profile."""
        response = self.client.post(
            reverse('add_child'),
            {
                'name': TEST_DATA["CHILD_NAME"],
                'birthdate': date.today()
            }
        )
        self.assertRedirects(response, reverse('profile'))
        self.assertTrue(
            Child.objects.filter(
                name=TEST_DATA["CHILD_NAME"],
                user=self.profile
            ).exists()
        )

    def test_confirm_delete_child_get(self):
        """Test GET request to confirm_delete_child view
        returns correct template."""
        child = Child.objects.create(
            name="DeleteMe",
            birthdate=date.today(),
            user=self.profile
        )
        url = reverse('confirm_delete_child', args=[child.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'children/confirm_delete_child.html')

    def test_confirm_delete_child_post(self):
        """Test POST request to confirm_delete_child view
        deletes the child and redirects to profile."""
        child = Child.objects.create(
            name="DeleteMe",
            birthdate=date.today(),
            user=self.profile
        )
        url = reverse('confirm_delete_child', args=[child.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('profile'))
        self.assertFalse(Child.objects.filter(id=child.id).exists())
