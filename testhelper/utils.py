from django.contrib.auth import get_user_model
from foods.models import Food
from profiles.models import Profile
from children.models import Child
from datetime import date

TEST_DATA = {
    "USERNAME": "testuser",
    "PASSWORD": "testpassword",
    "CHILD_NAME": "BridgeBaby",
}


def create_test_user_and_profile():
    """
    Create and return a test user and associated profile.

    Returns:
        tuple: (user, profile)
    """
    User = get_user_model()
    user = User.objects.create_user(
        username=TEST_DATA["USERNAME"], password=TEST_DATA["PASSWORD"]
    )
    profile = Profile.objects.create(user=user)
    return user, profile


def create_test_user_and_child():
    """
    Create and return a test user, profile, and child.

    Returns:
        tuple: (user, profile, child)
    """
    User = get_user_model()
    user = User.objects.create_user(
        username=TEST_DATA["USERNAME"], password=TEST_DATA["PASSWORD"]
    )
    profile = Profile.objects.create(user=user)
    child = Child.objects.create(
        name=TEST_DATA["CHILD_NAME"],
        birthdate=date.today(),
        user=profile,
    )
    return user, profile, child


def create_test_food(user=None):
    """
    Create and return a test Food instance.

    Args:
        user (User, optional): The user to associate as the creator.
        If not provided, uses the first user in the database.

    Returns:
        Food: The created Food instance.
    """
    if user is None:
        from django.contrib.auth import get_user_model
        user = get_user_model().objects.first()
    return Food.objects.create(
        name='Banana',
        category=0,
        min_age_months=6,
        is_allergen=False,
        image='banana.png',
        is_authorised=True,
        created_by_user_id=user.id,
    )
