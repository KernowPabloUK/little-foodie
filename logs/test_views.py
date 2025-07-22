from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from logs.models import (
    FoodLog,
    Consistency,
    FeedingMethod,
    Preparation,
    SatisfactionLevel
)
from testhelper.utils import (
    create_test_user_and_child,
    create_test_food,
    TEST_DATA,
)


class TestLogsViews(TestCase):
    """
    Test suite for the logs app views.

    This class contains tests to ensure that food log deletion and AJAX food
    creation behave as expected, including correct template rendering,
    database changes, and JSON responses for AJAX requests.
    """

    def setUp(self):
        """
        Set up a test user, profile, child, food, and related objects for
        use in tests.
        Logs in the test client and creates a sample FoodLog entry.
        """
        self.client = Client()
        self.user, self.profile, self.child = create_test_user_and_child()
        self.food = create_test_food(user=self.user)
        self.client.login(
            username=TEST_DATA["USERNAME"],
            password=TEST_DATA["PASSWORD"]
            )
        self.consistency = Consistency.objects.create(label=1)
        self.feeding_method = FeedingMethod.objects.create(label=1)
        self.preparation = Preparation.objects.create(label=1)
        self.satisfaction_level = SatisfactionLevel.objects.create(label=1)
        self.food_log = FoodLog.objects.create(
            food=self.food,
            child=self.child,
            user=self.user,
            favourite=True,
            logged_at=timezone.now(),
            volume=1,
            consistency=self.consistency,
            feeding_method=self.feeding_method,
            preparation=self.preparation,
            satisfaction_level=self.satisfaction_level
        )

    def test_delete_food_log_get(self):
        """
        Test that a GET request to delete_food_log renders the
        confirmation page.

        Ensures the correct template is used and the confirmation message
        is present.
        """
        url = reverse('delete_food_log', args=[self.food_log.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logs/delete_food_log.html')
        self.assertContains(
            response,
            "Are you sure you want to delete this Food Log?"
            )

    def test_delete_food_log_post(self):
        """
        Test that a POST request to delete_food_log deletes the log
        and redirects.

        Ensures the FoodLog is removed from the database and the user
        is redirected.
        """
        url = reverse('delete_food_log', args=[self.food_log.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('logs'))
        self.assertFalse(FoodLog.objects.filter(id=self.food_log.id).exists())

    def test_create_food_ajax_success(self):
        """
        Test that create_food_ajax creates a new food and
        returns a success JSON response.

        Ensures the food is created and the response contains the correct data.
        """
        url = reverse('create_food_ajax')
        data = {
            'name': 'Pear',
            'category': 0,
            'min_age_months': 6,
            'is_allergen': 'on'
        }
        response = self.client.post(
            url,
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data['success'])
        self.assertEqual(json_data['food']['name'], 'Pear')
        self.assertEqual(json_data['food']['category'], 'Fruit')

    def test_create_food_ajax_missing_fields(self):
        """
        Test that create_food_ajax returns an error if required fields
        are missing.

        Ensures the response contains an error message and success is False.
        """
        url = reverse('create_food_ajax')
        data = {'name': '', 'category': '', 'min_age_months': ''}
        response = self.client.post(
            url,
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertFalse(json_data['success'])
        self.assertIn('error', json_data)

    def test_create_food_ajax_duplicate(self):
        """
        Test that create_food_ajax returns an error if the food name
        already exists.

        Ensures the response contains an error message about duplication.
        """
        url = reverse('create_food_ajax')
        data = {
            'name': self.food.name,
            'category': self.food.category,
            'min_age_months': self.food.min_age_months,
            'is_allergen': 'on'
        }
        response = self.client.post(
            url,
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertFalse(json_data['success'])
        self.assertIn('already exists', json_data['error'])
