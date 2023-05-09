import pytest

from friends.models import FriendRequest, FriendShip


@pytest.mark.django_db
def test_get_incoming_requests(client, user1, user2, request_from_user2_to_user1):
    client.force_login(user1)
    response = client.get('/api/requests/?section=in')
    assert response.status_code == 200
    assert response.data[0]["from_user"] == request_from_user2_to_user1.from_user.username
    assert response.data[0]["to_user"] == request_from_user2_to_user1.to_user.username


@pytest.mark.django_db
def test_get_outgoing_requests(client, user1, user2, request_from_user1_to_user2):
    client.force_login(user1)
    response = client.get('/api/requests/?section=out')
    assert response.status_code == 200
    assert response.data[0]["from_user"] == request_from_user1_to_user2.from_user.username
    assert response.data[0]["to_user"] == request_from_user1_to_user2.to_user.username


@pytest.mark.django_db
def test_send_request_to_user(client, user1, user2):
    client.force_login(user1)
    body = {"to_user": "user2"}
    response = client.post(
        "/api/requests/",
        data=body,
        format="json"
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_mutual_friendship_request(client, user1, user2, request_from_user1_to_user2):
    client.force_login(user2)
    body = {"to_user": "user1"}
    response = client.post(
        '/api/requests/',
        data=body,
        format="json",
    )
    assert response.status_code == 201
    # check that friendship request has been deleted
    assert not FriendRequest.objects.filter(from_user=user1, to_user=user2).exists()
    assert FriendShip.objects.filter(user=user1, friend=user2).exists()
    assert FriendShip.objects.filter(user=user2, friend=user1).exists()


@pytest.mark.django_db
def test_approve_friends_request(client, user1, user2, request_from_user2_to_user1):
    client.force_login(user1)
    response = client.post(f'/api/requests/{user2.username}')
    assert response.status_code == 201
    assert FriendShip.objects.filter(user=user1, friend=user2).exists()
    assert FriendShip.objects.filter(user=user2, friend=user1).exists()
    assert not FriendRequest.objects.filter(from_user=user2, to_user=user1).exists()


@pytest.mark.django_db
def test_decline_friends_request(client, user1, user2, request_from_user2_to_user1):
    client.force_login(user1)
    response = client.delete(f'/api/requests/{user2.username}')
    assert response.status_code == 204
    assert not FriendRequest.objects.filter(from_user=user2, to_user=user1).exists()