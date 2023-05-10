from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import FriendRequest, FriendShip
from .serializers import FriendsRequestSerializer, FriendsSerializer


@swagger_auto_schema(
    method='get',
    responses={200: FriendsRequestSerializer(many=True)},
)
@swagger_auto_schema(
    method='post',
    request_body=FriendsRequestSerializer(),
    responses={201: FriendsRequestSerializer()},
)
@api_view(['GET', 'POST'])
def get_create_requests_view(request):
    """
    View for returning user friends requests and approving incoming request.

    :queryparam section: Specifies the type of friend requests to be returned.

    Allowed values:
        `in` - for incoming friend requests,
        `out` - for outcoming friend requests
    """
    if request.method == "GET":
        section = request.query_params.get('section')

        if section == "out":
            requests_ = FriendRequest.objects.filter(from_user=request.user)
            serializer = FriendsRequestSerializer(requests_, many=True)

        elif section == "in":
            requests_ = FriendRequest.objects.filter(to_user=request.user)
            serializer = FriendsRequestSerializer(requests_, many=True)

        return Response(serializer.data)

    elif request.method == "POST":
        from_user = request.user
        to_user = get_object_or_404(
            get_user_model(),
            username=request.data.get('to_user'),
        )
        mutual_request = FriendRequest.objects.filter(
            from_user=to_user,
            to_user=from_user,
        )
        if mutual_request.exists():
            friendship_records = (
                FriendShip(user=from_user, friend=to_user),
                FriendShip(user=to_user, friend=from_user)
            )
            FriendShip.objects.bulk_create(friendship_records)
            mutual_request.delete()
            return Response(status=status.HTTP_201_CREATED)

        else:
            serializer = FriendsRequestSerializer(
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST', 'DELETE'])
def approve_or_decline_friends_request_view(request, username):
    """View for approving or declining friendship request from user."""
    from_user = get_object_or_404(
        get_user_model(), username=username
    )

    friend_request = get_object_or_404(
        FriendRequest, from_user=from_user, to_user=request.user
    )
    friend_request.delete()

    if request.method == "POST":
        friendship_records = (
            FriendShip(user=request.user, friend=from_user),
            FriendShip(user=from_user, friend=request.user)
        )
        FriendShip.objects.bulk_create(friendship_records)
        return Response(status=status.HTTP_201_CREATED)

    elif request.method == "DELETE":
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_friends_view(request):
    """Return a list of friends for the authenticated user."""
    user_friends = FriendShip.objects.filter(
        user=request.user
    ).select_related("friend")
    serializer = FriendsSerializer(user_friends, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_friend_view(request, username):
    """View for deleting the friendship with the user with the given username."""
    friendship_record = get_object_or_404(
        FriendShip,
        user=request.user,
        friend=get_object_or_404(get_user_model(), username=username)
    )
    friendship_record.delete()
    FriendShip.objects.filter(
        user=get_object_or_404(get_user_model(), username=username),
        friend=request.user
    ).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_relationship_status_view(request, username):
    """Return the relationship status between current user and the given user."""
    with_user = get_object_or_404(
        get_user_model(), username=username,
    )

    if FriendShip.objects.filter(user=request.user, friend=with_user).exists():
        return Response(
            {"status": "friends"}
        )

    elif FriendRequest.objects.filter(
        from_user=request.user,
        to_user=with_user,
    ).exists():
        return Response(
            {"status": "request sent"}
        )

    elif FriendRequest.objects.filter(
        from_user=with_user,
        to_user=request.user,
    ).exists():
        return Response(
            {"status": "request received"}
        )

    else:
        return Response(
            {"status": "None"}
        )
