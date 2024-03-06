from django.urls import path, include

from user.views import (
    UserListView,
    UserCreateView,
    UserDetailView,
    UserUpdateView,
    UserDeleteView
)

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", UserListView.as_view(), name="user-list"),
    path("create/", UserCreateView.as_view(), name="user-create"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("<int:pk>/update/", UserUpdateView.as_view(), name="user-update"),
    path("<int:pk>/delete/", UserDeleteView.as_view(), name="user-delete"),
]

app_name = "user"
