from django.test import TestCase
from django.urls import reverse
from testhelper.utils import create_test_user_and_child, TEST_DATA
from children.models import Child
from children.forms import AddChildForm
from datetime import date


class TestChildrenViews(TestCase):
    def setUp(self):
        self.user, self.profile, self.child = create_test_user_and_child()
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
        """Test GET request to confirm_delete_child view
        returns correct template."""
        url = reverse('confirm_delete_child', args=[self.child.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'children/confirm_delete_child.html')

    def test_confirm_delete_child_post(self):
        """Test POST request to confirm_delete_child view
        deletes the child and redirects to profile."""
        url = reverse('confirm_delete_child', args=[self.child.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('profile'))
        self.assertFalse(Child.objects.filter(id=self.child.id).exists())
