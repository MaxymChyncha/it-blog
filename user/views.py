from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic

from config.utils.paginators import paginate_context
from user.forms import UserCreateForm, UserUpdateForm


class UserListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 5


class UserCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = UserCreateForm

    def get_success_url(self):
        return self.object.get_absolute_url()


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.object.posts.all()
        context = paginate_context(self.request, posts, context, 5)
        return context


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm

    def get_success_url(self):
        return self.object.get_absolute_url()


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()

    def get_success_url(self):
        return reverse("user:user-list")
