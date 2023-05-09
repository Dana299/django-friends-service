from django.contrib.auth import get_user_model
from django.db import models


class FriendRequest(models.Model):
    """ Model representing friend requests. """

    from_user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="out_requests"
    )
    to_user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="in_requests"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(from_user=models.F('to_user')),
                name='different_users',
            )
        ]

    def __str__(self):
        return f"Friend request from {self.from_user} to {self.to_user}"


class FriendShip(models.Model):
    """ Model representing friendship between two users. """

    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="friends"
    )
    friend = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend',)
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user=models.F('friend')),
                name='different_friends',
            )
        ]

    def __str__(self):
        return f"Friendship between {self.user} and {self.friend}"
