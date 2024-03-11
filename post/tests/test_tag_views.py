from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from post.models import Tag

TAG_PK = 1
TAG_LIST_URL = reverse("post:tag-list")
TAG_CREATE_URL = reverse("post:tag-create")
TAG_DETAIL_URL = reverse("post:tag-detail", kwargs={"pk": TAG_PK})
TAG_UPDATE_URL = reverse("post:tag-update", kwargs={"pk": TAG_PK})
TAG_DELETE_URL = reverse("post:tag-delete", kwargs={"pk": TAG_PK})


class PublicTagViewTest(TestCase):

    def test_login_required(self):
        for url in (
                TAG_LIST_URL,
                TAG_CREATE_URL,
                TAG_DETAIL_URL,
                TAG_UPDATE_URL,
                TAG_DELETE_URL,
        ):
            res = self.client.get(url)

            self.assertNotEqual(res.status_code, 200)


class PrivateTagViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.tag_1 = Tag.objects.create(
            name="python"
        )
        self.tag_2 = Tag.objects.create(
            name="java"
        )

        self.client.force_login(self.user)

    def test_tag_retrieve(self):
        res = self.client.get(TAG_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context.get("tag_list")),
            list(Tag.objects.all())
        )
        self.assertTemplateUsed(res, "post/tag_list.html")

    def test_tag_retrieve_search_filter(self):
        url = f"{TAG_LIST_URL}?name=ja"
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertIn("search_form", res.context)
        self.assertEqual(list(res.context.get("tag_list")), [self.tag_2])

    def test_tag_create_get_success_url(self):
        data = {"name": "New tag"}
        res = self.client.post(TAG_CREATE_URL, data=data)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, TAG_LIST_URL)

    def test_tag_detail_get_context_data(self):
        res = self.client.get(TAG_DETAIL_URL)

        self.assertIn("paginated_obj", res.context)
        self.assertIn("paginated_obj", res.context)
        self.assertIn("paginator", res.context)
        self.assertIn("page_obj", res.context)
        self.assertIn("is_paginated", res.context)

    def test_tag_update_get_success_url(self):
        data = {"name": "New tag"}
        res = self.client.post(TAG_UPDATE_URL, data=data)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, TAG_LIST_URL)

    def test_tag_delete_get_success_url(self):
        res = self.client.delete(TAG_DELETE_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, TAG_LIST_URL)
