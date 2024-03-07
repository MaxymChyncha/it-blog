from django.contrib.auth import get_user_model
from django.test import TestCase

from user.forms import UserCreateForm, UserUpdateForm


class UserCreateFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            "username": "new_user",
            "first_name": "first",
            "last_name": "last",
            "password1": "test_1234",
            "password2": "test_1234"
        }
        form = UserCreateForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_invalid_form(self):
        form_data = {
            "username": "new_user",
            "first_name": "first",
            "last_name": "last",
            "password1": "test_1234",
            "password2": "test_12345"
        }
        form = UserCreateForm(data=form_data)

        self.assertFalse(form.is_valid())


class UserUpdateFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            first_name="first",
            last_name="last"
        )

    def test_valid_form(self):
        form_data = {"username": "new_username"}
        form = UserUpdateForm(
            data=form_data,
            instance=self.user
        )

        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {"username": ""}
        form = UserCreateForm(
            data=form_data,
            instance=self.user
        )

        self.assertFalse(form.is_valid())
