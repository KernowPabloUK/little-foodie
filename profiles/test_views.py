from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from profiles.models import Profile


class TestProfileViews(TestCase):
    """Tests for profile-related views."""

    def setUp(self):
        """Create a test user and profile."""
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass'
        )
        self.profile = Profile.objects.create(user=self.user)

    def test_home_view_accessible(self):
        """Home view should be accessible to all users."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/home.html')

    def test_profile_view_requires_login(self):
        """Profile view should redirect anonymous users to login."""
        response = self.client.get(reverse('profile'))
        self.assertNotEqual(response.status_code, 200)
        self.assertIn('/login', response.url)

    def test_profile_view_loads_for_logged_in_user(self):
        """Profile view should load for authenticated users."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        self.assertContains(response, self.user.username)

    def test_profile_update_success(self):
        """Profile view should update profile on valid POST."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('profile'),
            data={'first_name': 'Sam', 'last_name': 'Porter', 'birth_date': '1990-01-01'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.first_name, 'Sam')
        self.assertContains(response, 'Profile updated successfully!')
