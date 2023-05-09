import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from friends.models import FriendRequest, FriendShip


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user1():
    return get_user_model().objects.create_user(
        'user1',
        'password'
    )


@pytest.fixture
def user2():
    return get_user_model().objects.create_user(
        'user2',
        'password'
    )


@pytest.fixture
def request_from_user1_to_user2(user1, user2):
    return FriendRequest.objects.create(
        from_user=user1,
        to_user=user2,
    )


@pytest.fixture
def friendship(user1, user2):
    FriendShip.objects.create(user=user1, friend=user2)
    FriendShip.objects.create(user=user2, friend=user1)


@pytest.fixture
def request_from_user2_to_user1(user1, user2):
    return FriendRequest.objects.create(
        from_user=user2,
        to_user=user1,
    )
