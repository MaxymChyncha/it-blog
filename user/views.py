from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.views import generic

from config.utils.paginators import paginate_context
from user.forms import UserCreateForm, UserUpdateForm, UserSearchForm


class UserListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 8

    def get_queryset(self) -> QuerySet:
        queryset = super(UserListView, self).get_queryset()
        queryset = (
            queryset.prefetch_related("comments").prefetch_related("posts")
        )
        form = UserSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data.get("username")
            )

        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super(UserListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username")
        context["search_form"] = UserSearchForm(
            initial={"username": username}
        )
        return context


class UserCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = UserCreateForm

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        posts = self.object.posts.all()
        context = paginate_context(self.request, posts, context, 8)
        return context


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()

    def get_success_url(self) -> str:
        return reverse("user:user-list")
