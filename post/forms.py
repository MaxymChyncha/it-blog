from django import forms

from post.models import Comment


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        labels = {"content": "Add comment:"}


class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
