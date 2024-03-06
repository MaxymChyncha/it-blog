from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin

from config.utils.paginators import paginate_queryset
from post.forms import CommentCreateForm
from post.models import Post, Tag, Comment


class PostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    paginate_by = 5
    template_name = "post/post_list.html"

    def get_queryset(self):
        queryset = super(PostListView, self).get_queryset()
        queryset = (queryset
                    .select_related("author")
                    .prefetch_related("comments")
                    )
        return queryset


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ("tag", "title", "content",)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class PostDetailView(LoginRequiredMixin, FormMixin, generic.DetailView):
    model = Post
    form_class = CommentCreateForm

    def get_queryset(self):
        queryset = super(PostDetailView, self).get_queryset()
        queryset = (queryset
                    .select_related("author")
                    .prefetch_related("comments__author")
                    )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        comments = self.object.comments.all()
        paginated_comments = paginate_queryset(self.request, comments, 5)
        context["comments"] = paginated_comments
        context["paginator"] = paginated_comments.paginator
        context["page_obj"] = paginated_comments
        context["is_paginated"] = paginated_comments.has_other_pages()

        context["form"] = CommentCreateForm(
            initial={"post": self.object, "author": self.request.user}
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.get_object()
        form.save()
        return super(PostDetailView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ("title", "content",)

    def get_success_url(self):
        return self.object.get_absolute_url()


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post

    def get_success_url(self):
        return reverse("post:post-list")


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    fields = ("name",)

    def get_success_url(self):
        return reverse("post:tag-list")


class TagDetailView(LoginRequiredMixin, generic.DetailView):
    model = Tag

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        posts = self.object.posts.all()
        paginated_posts = paginate_queryset(self.request, posts, 5)
        context["posts"] = paginated_posts
        context["paginator"] = paginated_posts.paginator
        context["page_obj"] = paginated_posts
        context["is_paginated"] = paginated_posts.has_other_pages()

        return context


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    fields = ("name",)

    def get_success_url(self):
        return reverse("post:tag-list")


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag

    def get_success_url(self):
        return reverse("post:tag-list")


class CommentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Comment

    def get_success_url(self):
        post_pk = self.object.post_id
        return reverse("post:post-detail", kwargs={"pk": post_pk})
