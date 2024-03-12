from django.contrib.auth import get_user_model
from django.test import TestCase

from post.models import Post, Comment, Tag


class PostModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="1234test"
        )
        self.post = Post.objects.create(
            author=self.user,
            title="title",
            content="content"
        )

    def test_comments_counter(self):
        self.post.comments.create(
            author=self.user,
            content="comment_1"
        )
        self.post.comments.create(
            author=self.user,
            content="comment_2"
        )

        self.assertEqual(self.post.comments_counter, 2)

    def test_get_absolute_url(self):
        self.assertEqual(
            self.post.get_absolute_url(),
            "/posts/1/"
        )

    def test_post_str(self):
        self.assertEqual(
            str(self.post),
            f"Title: {self.post.title}. "
            f"Author: {self.post.author.username}"
        )


class CommentModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="1234test"
        )
        self.post = Post.objects.create(
            author=self.user,
            title="title",
            content="content"
        )
        self.comment = Comment.objects.create(
            author=self.user,
            post=self.post,
            content="comment"
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.comment.get_absolute_url(),
            "/posts/1/"
        )

    def test_comment_str(self):
        self.assertEqual(
            str(self.comment),
            f"Content: {self.comment.content[:10]}. "
            f"Author: {self.comment.author.username}"
        )


class TagModelTest(TestCase):
    
    def setUp(self):
        self.tag = Tag.objects.create(name="test")

    def test_get_absolute_url(self):
        self.assertEqual(
            self.tag.get_absolute_url(),
            "/tags/1/"
        )

    def test_comment_str(self):
        self.assertEqual(
            str(self.tag),
            self.tag.name
        )
