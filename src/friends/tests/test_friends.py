import pytest

from friends.models import FriendShip


@pytest.mark.django_db
def test_friends_list(client, user1, user2):
    client.force_login(user1)
    response = client.get('/api/friends/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_friend(client, user1, user2, friendship):
    client.force_login(user1)
    response = client.delete(f'/api/friends/{user2.username}')
    assert response.status_code == 204
    assert not FriendShip.objects.filter(user=user1, friend=user2).exists()
    assert not FriendShip.objects.filter(user=user2, friend=user1).exists()


@pytest.mark.django_db
def test_get_relations_status_friends(client, user1, user2, friendship):
    client.force_login(user1)
    response = client.get(f'/api/friends/status/{user2.username}')
    assert response.status_code == 200
    assert response.data == {"status": "friends"}


@pytest.mark.django_db
def test_get_relations_status_incoming_request(
    client,
    user1,
    user2,
    request_from_user2_to_user1
):
    client.force_login(user1)
    response = client.get(f'/api/friends/status/{user2.username}')
    assert response.status_code == 200
    assert response.data == {"status": "request received"}


@pytest.mark.django_db
def test_get_relations_status_outcoming_request(
    client,
    user1,
    user2,
    request_from_user1_to_user2
):
    client.force_login(user1)
    response = client.get(f'/api/friends/status/{user2.username}')
    assert response.status_code == 200
    assert response.data == {"status": "request sent"}


@pytest.mark.django_db
def test_get_relations_status_none(client, user1, user2):
    client.force_login(user1)
    response = client.get(f'/api/friends/status/{user2.username}')
    assert response.status_code == 200
    assert response.data == {"status": "None"}
