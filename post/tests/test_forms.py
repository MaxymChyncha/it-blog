from django.contrib.auth import get_user_model
from django.test import TestCase

from post.forms import (
    CommentCreateForm,
    CommentUpdateForm,
    PostSearchForm,
    TagSearchForm
)
from post.models import Comment, Post


class CommentCreateFormTest(TestCase):

    def test_valid_form(self):
        form_data = {"content": "Valid content"}
        form = CommentCreateForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_invalid_form(self):
        form_data = {"content": ""}
        form = CommentCreateForm(data=form_data)

        self.assertFalse(form.is_valid())


class CommentUpdateFormTest(TestCase):

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
        self.comment = Comment(
            author=self.user,
            post=self.post,
            content="content"
        )

    def test_valid_form(self):
        form_data = {"content": "New content"}
        form = CommentUpdateForm(
            data=form_data,
            instance=self.comment
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_invalid_form(self):
        form_data = {"content": ""}
        form = CommentUpdateForm(
            data=form_data,
            instance=self.comment
        )

        self.assertFalse(form.is_valid())


class PostSearchFormTest(TestCase):

    def setUp(self):
        self.form = PostSearchForm()

    def test_model_field_placeholder(self):
        self.assertEqual(
            self.form.fields["title"].widget.attrs["placeholder"],
            "Search by title"
        )

    def test_model_field_not_required(self):
        self.assertFalse(self.form.fields["title"].required)


class TagSearchFormTest(TestCase):

    def setUp(self):
        self.form = TagSearchForm()

    def test_model_field_placeholder(self):
        self.assertEqual(
            self.form.fields["name"].widget.attrs["placeholder"],
            "Search by name"
        )

    def test_model_field_not_required(self):
        self.assertFalse(self.form.fields["name"].required)
