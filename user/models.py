from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    class Meta:
        ordering = ("username",)

    @property
    def posts_counter(self) -> int:
        return self.posts.count()

    @property
    def comments_counter(self) -> int:
        return self.comments.count()

    def get_absolute_url(self) -> str:
        return reverse("user:user-detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"
