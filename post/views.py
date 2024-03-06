from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin

from post.forms import CommentCreateForm
from post.models import Post, Tag, Comment


class PostListView(generic.ListView):
    model = Post
    paginate_by = 5
    template_name = "post/post_list.html"

    def get_queryset(self):
        queryset = super(PostListView, self).get_queryset()
        queryset = queryset.select_related("author").prefetch_related("comments")
        return queryset


class PostCreateView(generic.CreateView):
    model = Post
    fields = "__all__"

    def get_success_url(self):
        return self.object.get_absolute_url()


class PostDetailView(FormMixin, generic.DetailView):
    model = Post
    form_class = CommentCreateForm

    def get_queryset(self):
        queryset = super(PostDetailView, self).get_queryset()
        queryset = queryset.select_related("author").prefetch_related("comments__author")
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
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


class PostUpdateView(generic.UpdateView):
    model = Post
    fields = ("title", "content",)

    def get_success_url(self):
        return self.object.get_absolute_url()


class PostDeleteView(generic.DeleteView):
    model = Post

    def get_success_url(self):
        return reverse("post:post-list")


class TagListView(generic.ListView):
    model = Tag


class TagCreateView(generic.CreateView):
    model = Tag
    fields = ("name",)

    def get_success_url(self):
        return reverse("post:tag-list")


class TagDetailView(generic.DetailView):
    model = Tag


class TagUpdateView(generic.UpdateView):
    model = Tag
    fields = ("name",)

    def get_success_url(self):
        return reverse("post:tag-list")


class TagDeleteView(generic.DeleteView):
    model = Tag

    def get_success_url(self):
        return reverse("post:tag-list")


class CommentDeleteView(generic.DeleteView):
    model = Comment

    def get_success_url(self):
        post_pk = self.object.post_id
        return reverse("post:post-detail", kwargs={"pk": post_pk})
