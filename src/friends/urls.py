from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView
from django.urls import include, path

from .views import (approve_or_decline_friends_request_view,
                    delete_friend_view, get_create_requests_view,
                    get_friends_view, get_relationship_status_view)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path(
        "requests/",
        include(
            [
                path("", get_create_requests_view, name="requests"),
                path("<str:username>", approve_or_decline_friends_request_view),
            ]
        )
    ),
    path(
        "friends/",
        include(
            [
                path("", get_friends_view),
                path("<str:username>", delete_friend_view, name="delete_friend"),
                path(
                    "status/<str:username>",
                    get_relationship_status_view,
                    name="relationship-status"
                ),
            ]
        )
    )
]
