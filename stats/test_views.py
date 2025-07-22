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
    TEST_DATA)


class TestStatisticsView(TestCase):
    def setUp(self):
        self.user, self.profile, self.child = create_test_user_and_child(
            username=TEST_DATA["USERNAME"], password=TEST_DATA["PASSWORD"]
        )
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
        """Statistics view should redirect anonymous users to login."""
        response = self.client.get(reverse('stats'))
        self.assertNotEqual(response.status_code, 200)
        self.assertIn('/login', response.url)

    def test_statistics_view_loads_for_logged_in_user(self):
        """Statistics view should load for authenticated users
        and contain expected context."""
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
