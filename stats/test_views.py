from django.test import TestCase
from django.urls import reverse
from logs.models import (
    FoodLog,
    Consistency,
    FeedingMethod,
    Preparation,
    SatisfactionLevel,
)
from django.utils import timezone
from testhelper.utils import (
    create_test_user_and_child,
    create_test_food,
    TEST_DATA
)


class TestStatisticsView(TestCase):
    """
    Test suite for the statistics view in the stats app.

    This class contains tests to ensure that the statistics view requires
    authentication, loads correctly for logged-in users, and provides the
    expected context data.
    """

    def setUp(self):
        """
        Set up a test user, profile, child, food, and related objects for use
        in tests.
        Creates a sample FoodLog entry for statistics calculations.
        """
        self.user, self.profile, self.child = create_test_user_and_child()
        self.food = create_test_food(user=self.user)
        self.consistency = Consistency.objects.create(label=1)
        self.feeding_method = FeedingMethod.objects.create(label=1)
        self.preparation = Preparation.objects.create(label=1)
        self.satisfaction_level = SatisfactionLevel.objects.create(label=1)
        FoodLog.objects.create(
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

    def test_statistics_view_requires_login(self):
        """
        Test that the statistics view redirects anonymous users to the
        login page.
        """
        response = self.client.get(reverse('stats'))
        self.assertNotEqual(response.status_code, 200)
        self.assertIn('/login', response.url)

    def test_statistics_view_loads_for_logged_in_user(self):
        """
        Test that the statistics view loads for authenticated users and
        contains expected context data.
        """
        self.client.login(
            username=TEST_DATA["USERNAME"], password=TEST_DATA["PASSWORD"]
        )
        session = self.client.session
        session['selected_child_id'] = self.child.id
        session.save()
        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stats/statistics.html')
        self.assertIn('food_stats', response.context)
        self.assertIn('category_stats', response.context)
        self.assertIn('children', response.context)
        self.assertIn('selected_child', response.context)
        self.assertContains(response, 'Banana')
