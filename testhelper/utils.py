from django.contrib.auth import get_user_model
from profiles.models import Profile
from children.models import Child
from datetime import date

TEST_DATA = {
    "USERNAME": "testuser",
    "PASSWORD": "testpassword",
    "CHILD_NAME": "BridgeBaby",
}


def create_test_user_and_profile():
    User = get_user_model()
    user = User.objects.create_user(
        username=TEST_DATA["USERNAME"], password=TEST_DATA["PASSWORD"]
    )
    profile = Profile.objects.create(user=user)
    return user, profile


def create_test_user_and_child():
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
