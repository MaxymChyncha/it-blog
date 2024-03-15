from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin

from config.utils.paginators import paginate_context
from post.forms import (
    CommentCreateForm,
    CommentUpdateForm,
    PostSearchForm,
    TagSearchForm, PostCreateForm
)
from post.models import Post, Tag, Comment


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "post/index.html")


class PostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    paginate_by = 8
    template_name = "post/post_list.html"

    def get_queryset(self) -> QuerySet:
        queryset = super(PostListView, self).get_queryset()
        queryset = (
            queryset.select_related("author").prefetch_related("comments")
        )
        form = PostSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                title__icontains=form.cleaned_data.get("title")
            )

        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super(PostListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title")
        context["search_form"] = PostSearchForm(
            initial={"title": title}
        )
        return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostCreateForm

    def form_valid(self, form: PostCreateForm):
        form.instance.author = self.request.user
        form.save()
        return super(PostCreateView, self).form_valid(form)

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()


class PostDetailView(LoginRequiredMixin, FormMixin, generic.DetailView):
    model = Post
    form_class = CommentCreateForm

    def get_queryset(self) -> QuerySet:
        queryset = super(PostDetailView, self).get_queryset()
        queryset = (
            queryset.select_related("author").prefetch_related("comments__author")
        )
        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super(PostDetailView, self).get_context_data(**kwargs)
        comments = self.object.comments.all()
        context = paginate_context(self.request, comments, context, 8)

        context["form"] = CommentCreateForm(
            initial={"post": self.object, "author": self.request.user}
        )
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form: CommentCreateForm):
        form.instance.author = self.request.user
        form.instance.post = self.get_object()
        form.save()
        return super(PostDetailView, self).form_valid(form)

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ("title", "content",)

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post

    def get_success_url(self) -> str:
        return reverse("post:post-list")


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    paginate_by = 8

    def get_queryset(self) -> QuerySet:
        queryset = super(TagListView, self).get_queryset()
        queryset = queryset.prefetch_related("posts")

        form = TagSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data.get("name")
            )
        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super(TagListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["search_form"] = TagSearchForm(
            initial={"name": name}
        )
        return context


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    fields = ("name",)

    def get_success_url(self) -> str:
        return reverse("post:tag-list")


class TagDetailView(LoginRequiredMixin, generic.DetailView):
    model = Tag

    def get_context_data(self, **kwargs) -> dict:
        context = super(TagDetailView, self).get_context_data(**kwargs)
        posts = self.object.posts.prefetch_related("tag")
        context = paginate_context(self.request, posts, context, 8)
        return context


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    fields = ("name",)

    def get_success_url(self) -> str:
        return reverse("post:tag-list")


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag

    def get_success_url(self) -> str:
        return reverse("post:tag-list")


class CommentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Comment
    form_class = CommentUpdateForm

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Comment

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()
