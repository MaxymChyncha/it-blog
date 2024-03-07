from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="1234test"
        )
        self.post_1 = self.user.posts.create(
            title="title_1",
            content="content_1"
        )
        self.post_2 = self.user.posts.create(
            title="title_2",
            content="content_2"
        )

    def test_posts_counter(self):
        self.assertEqual(self.user.posts_counter, 2)

    def test_comments_counter(self):
        self.post_1.comments.create(
            author=self.user,
            content="comment_content_1"
        )
        self.post_2.comments.create(
            author=self.user,
            content="comment_content_2"
        )
        self.assertEqual(self.user.comments_counter, 2)

    def test_get_absolute_url(self):
        self.assertEqual(
            self.user.get_absolute_url(),
            "/user/1/"
        )

    def test_user_str(self):
        self.assertEqual(
            str(self.user),
            f"{self.user.username} "
            f"({self.user.first_name} {self.user.last_name})"
        )
