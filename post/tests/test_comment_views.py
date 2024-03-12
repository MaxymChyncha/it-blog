from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from post.models import Post, Comment

COMMENT_PK = 1
COMMENT_UPDATE_URL = reverse("post:comment-update", kwargs={"pk": COMMENT_PK})
COMMENT_DELETE_URL = reverse("post:comment-delete", kwargs={"pk": COMMENT_PK})


class PublicCommentViewTest(TestCase):

    def test_login_required(self):
        for url in (
                COMMENT_UPDATE_URL,
                COMMENT_DELETE_URL,
        ):
            res = self.client.get(url)

            self.assertNotEqual(res.status_code, 200)


class PrivateCommentViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.post = Post.objects.create(
            author=self.user,
            title="title",
            content="content"
        )
        self.comment = Comment.objects.create(
            author=self.user,
            post=self.post,
            content="content"
        )

        self.client.force_login(self.user)

    def test_comment_update_get_success_url(self):
        data = {
            "author": self.user.id,
            "post": self.post.id,
            "content": "New content"
        }
        res = self.client.post(COMMENT_UPDATE_URL, data=data)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.comment.get_absolute_url())

    def test_comment_delete_get_success_url(self):
        res = self.client.delete(COMMENT_DELETE_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.comment.get_absolute_url())
