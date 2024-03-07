from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from post.models import Post, Tag, Comment

POST_PK = 1
POST_LIST_URL = reverse("post:post-list")
POST_CREATE_URL = reverse("post:post-create")
POST_DETAIL_URL = reverse("post:post-detail", kwargs={"pk": POST_PK})
POST_UPDATE_URL = reverse("post:post-update", kwargs={"pk": POST_PK})
POST_DELETE_URL = reverse("post:post-delete", kwargs={"pk": POST_PK})


class PublicPostViewTest(TestCase):

    def test_login_required(self):
        for url in (
                POST_LIST_URL,
                POST_CREATE_URL,
                POST_DETAIL_URL,
                POST_UPDATE_URL,
                POST_DELETE_URL,
        ):
            res = self.client.get(url)

            self.assertNotEqual(res.status_code, 200)


class PrivatePostViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.tag = Tag.objects.create(
            name="python"
        )
        self.post_1 = Post.objects.create(
            author=self.user,
            title="title_1",
            content="content_1"
        )
        self.post_2 = Post.objects.create(
            author=self.user,
            title="title_2",
            content="content_2"
        )

        self.client.force_login(self.user)

    def test_post_retrieve(self):
        res = self.client.get(POST_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["post_list"]),
            list(Post.objects.all())
        )
        self.assertTemplateUsed(res, "post/post_list.html")

    def test_post_retrieve_search_filter(self):
        url = f"{POST_LIST_URL}?title=2"
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertIn("search_form", res.context)
        self.assertEqual(list(res.context["post_list"]), [self.post_2])

    def test_post_create_author_equal_current_logged_user(self):
        data = {
            "tag": self.tag.id,
            "title": "Test title",
            "content": "Test content"
        }
        res = self.client.post(POST_CREATE_URL, data=data)
        post = Post.objects.latest("id")

        self.assertEqual(res.status_code, 302)
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.title, "Test title")

    def test_post_create_get_success_url(self):
        data = {
            "tag": self.tag.id,
            "title": "Test title",
            "content": "Test content"
        }
        res = self.client.post(POST_CREATE_URL, data=data)
        post = Post.objects.latest("id")

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, post.get_absolute_url())

    def test_post_detail_get_context_data(self):
        res = self.client.get(POST_DETAIL_URL)

        self.assertIn("paginated_obj", res.context)
        self.assertIn("paginator", res.context)
        self.assertIn("page_obj", res.context)
        self.assertIn("is_paginated", res.context)
        self.assertIn("form", res.context)

    def test_post_detail_create_comment_with_valid_data(self):
        data = {
            "author": self.user.id,
            "post": self.post_1.id,
            "content": "Content"
        }
        res = self.client.post(POST_DETAIL_URL, data=data)
        comments = Comment.objects.filter(post=self.post_1)

        self.assertEqual(res.status_code, 302)
        self.assertEqual(comments.count(), 1)
        self.assertEqual(comments.latest("id").content, "Content")

    def test_post_detail_create_comment_with_invalid_data(self):
        data = {
            "author": self.user.id,
            "post": self.post_1.id,
            "content": ""
        }
        res = self.client.post(POST_DETAIL_URL, data=data)
        comments = Comment.objects.filter(post=self.post_1)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(comments.count(), 0)

    def test_post_detail_get_success_url(self):
        data = {
            "author": self.user.id,
            "post": self.post_1.id,
            "content": "Content"
        }
        res = self.client.post(POST_DETAIL_URL, data)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.post_1.get_absolute_url())

    def test_post_update_get_success_url(self):
        data = {
            "tag": self.tag.id,
            "title": "New title",
            "content": "New Content"
        }
        res = self.client.post(POST_UPDATE_URL, data)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.post_1.get_absolute_url())

    def test_post_delete_get_success_url(self):
        res = self.client.delete(POST_DELETE_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, POST_LIST_URL)
