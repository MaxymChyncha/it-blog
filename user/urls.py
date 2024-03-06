from django.urls import path, include

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
]

app_name = "user"
