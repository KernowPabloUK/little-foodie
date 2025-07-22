from django.test import TestCase
from django.urls import reverse
from testhelper.utils import (
    create_test_user_and_child,
    create_test_food,
    TEST_DATA,
)
from logs.models import (
    FoodLog,
    Consistency,
    FeedingMethod,
    Preparation,
    SatisfactionLevel,
    )
from django.utils import timezone


class TestFoodViews(TestCase):
    def setUp(self):
        self.user, self.profile, self.child = create_test_user_and_child()
        self.food = create_test_food()
        self.client.login(
            username=TEST_DATA["USERNAME"],
            password=TEST_DATA["PASSWORD"]
        )

    def test_food_view_requires_login(self):
        """Test that food_view redirects to login
        for anonymous users and loads for logged in"""
        self.client.logout()
        response = self.client.get(reverse('foods'))
        self.assertNotEqual(response.status_code, 200)
        self.client.login(
            username=TEST_DATA["USERNAME"],
            password=TEST_DATA["PASSWORD"]
            )
        response = self.client.get(reverse('foods'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foods/food.html')

    def test_food_view_renders_template(self):
        """Test that food_view returns 200 and uses the correct template"""
        response = self.client.get(reverse('foods'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foods/food.html')

    def test_food_details_api_unauthenticated(self):
        """Test food_details_api returns correct data
        for unauthenticated user"""
        self.client.logout()
        url = reverse('food_details_api', args=[self.food.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['id'], self.food.id)
        self.assertEqual(data['name'], self.food.name)
        self.assertEqual(data['category'], self.food.get_category_display())
        self.assertEqual(data['min_age_months'], self.food.min_age_months)
        self.assertEqual(data['is_allergen'], self.food.is_allergen)
        self.assertIn('banana.png', data['image'])
        self.assertFalse(data['is_favourite'])
        self.assertTrue(data['is_authorised'])

    def test_food_details_api_favourite(self):
        """Test food_details_api returns is_favourite=True
        if recent log exists for selected child"""
        session = self.client.session
        session['selected_child_id'] = self.child.id
        session.save()

        consistency = Consistency.objects.create(label=1)
        feeding_method = FeedingMethod.objects.create(label=1)
        preparation = Preparation.objects.create(label=1)
        satisfaction_level = SatisfactionLevel.objects.create(label=1)

        FoodLog.objects.create(
            food=self.food,
            child=self.child,
            user=self.user,
            favourite=True,
            logged_at=timezone.now(),
            volume=1,
            consistency=consistency,
            feeding_method=feeding_method,
            preparation=preparation,
            satisfaction_level=satisfaction_level
        )
        url = reverse('food_details_api', args=[self.food.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['is_favourite'])

    def test_food_details_api_authenticated(self):
        """Test food_details_api returns
        correct data for authenticated user"""
        url = reverse('food_details_api', args=[self.food.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['id'], self.food.id)
        self.assertEqual(data['name'], self.food.name)
        self.assertEqual(data['category'], self.food.get_category_display())
        self.assertEqual(data['min_age_months'], self.food.min_age_months)
        self.assertEqual(data['is_allergen'], self.food.is_allergen)
        self.assertIn('banana.png', data['image'])
        self.assertFalse(data['is_favourite'])
        self.assertTrue(data['is_authorised'])
