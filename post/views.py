from django.urls import reverse
from django.views import generic

from post.models import Post


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


class PostDetailView(generic.DetailView):
    model = Post

    def get_queryset(self):
        queryset = super(PostDetailView, self).get_queryset()
        queryset = queryset.prefetch_related("comments")
        return queryset


class PostUpdateView(generic.UpdateView):
    model = Post
    fields = ("title", "content",)

    def get_success_url(self):
        return self.object.get_absolute_url()


class PostDeleteView(generic.DeleteView):
    model = Post

    def get_success_url(self):
        return reverse("post:post-list")
