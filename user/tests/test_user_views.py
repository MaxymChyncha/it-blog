from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

USER_PK = 1
USER_LIST_URL = reverse("user:user-list")
USER_CREATE_URL = reverse("user:user-create")
USER_DETAIL_URL = reverse("user:user-detail", kwargs={"pk": USER_PK})
USER_UPDATE_URL = reverse("user:user-update", kwargs={"pk": USER_PK})
USER_DELETE_URL = reverse("user:user-delete", kwargs={"pk": USER_PK})


class PublicUserViewTest(TestCase):

    def test_login_required(self):
        for url in (
                USER_LIST_URL,
                USER_CREATE_URL,
                USER_DETAIL_URL,
                USER_UPDATE_URL,
                USER_DELETE_URL,
        ):
            res = self.client.get(url)

            self.assertNotEqual(res.status_code, 200)


class PrivateUserViewTest(TestCase):
    def setUp(self):
        self.user_1 = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.user_2 = get_user_model().objects.create_user(
            username="test_2",
            password="test1234"
        )

        self.client.force_login(self.user_1)

    def test_user_retrieve(self):
        res = self.client.get(USER_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context.get("user_list")),
            list(get_user_model().objects.all())
        )
        self.assertTemplateUsed(res, "user/user_list.html")

    def test_user_retrieve_search_filter(self):
        url = f"{USER_LIST_URL}?username=_2"
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertIn("search_form", res.context)
        self.assertEqual(list(res.context.get("user_list")), [self.user_2])

    def test_user_create_get_success_url(self):
        data = {
            "username": "new_user",
            "first_name": "first",
            "last_name": "last",
            "password1": "test_1234",
            "password2": "test_1234"
        }
        res = self.client.post(USER_CREATE_URL, data=data)
        user = get_user_model().objects.latest("id")

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, user.get_absolute_url())

    def test_user_detail_get_context_data(self):
        res = self.client.get(USER_DETAIL_URL)

        self.assertIn("paginated_obj", res.context)
        self.assertIn("paginator", res.context)
        self.assertIn("page_obj", res.context)
        self.assertIn("is_paginated", res.context)

    def test_user_update_get_success_url(self):
        data = {
            "username": "new_name"
        }
        res = self.client.post(USER_UPDATE_URL, data)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.user_1.get_absolute_url())

    def test_user_delete_get_success_url(self):
        res = self.client.delete(USER_DELETE_URL)

        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, USER_LIST_URL)
