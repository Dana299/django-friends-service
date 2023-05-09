from django.contrib import admin

from .models import FriendRequest, FriendShip

admin.site.register(FriendShip)
admin.site.register(FriendRequest)
