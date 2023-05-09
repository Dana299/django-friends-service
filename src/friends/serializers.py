from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import FriendRequest, FriendShip


class FriendsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="friend.username")

    class Meta:
        model = FriendShip
        fields = ("username", )


class FriendsRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.StringRelatedField()
    to_user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=get_user_model().objects.all(),
    )

    class Meta:
        model = FriendRequest
        fields = ("from_user", "to_user", "created_at")

    def create(self, validated_data):
        validated_data["from_user"] = self.context['request'].user
        return FriendRequest.objects.create(**validated_data)
