from django.contrib.auth import get_user_model
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="posts"
    )
    tag = models.ManyToManyField(
        to=Tag,
        related_name="posts"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"Title: {self.title}. Author: {self.author.username}"


class Comment(models.Model):
    author = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="comments"
    )
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Content: {self.content[:10]}. Author: {self.author.username}"
