import random
import secrets

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        new_user = form.save()
        new_user.is_active = False
        token = secrets.token_hex(8)
        new_user.token = token
        new_user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/confirm/{token}'
        send_mail(
            subject="Подтверждение регистрации",
            message=f'Перейдите по ссылке для подтверждение регистрации {url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)

def email_verification(request, token):
    new_user = get_object_or_404(User, token=token)
    new_user.is_active = True
    new_user.save()
    return redirect(reverse_lazy("users:login"))


class UserUpdateView(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("users:user_list")
    login_url = "users:login"
    permission_required = "users.change_user"

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for x in range(8)])
    request.user.set_password(new_password)
    request.user.save()
    send_mail(
        subject="Изменение пароля",
        message=f"Ваш пароль был изменен. Новый пароль:{new_password}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    return redirect(reverse_lazy('mailing:home'))


class UserListView(ListView, PermissionRequiredMixin):
    model = User
    permission_required = "users.view_user"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data["users_list"] = User.objects.all()
        return context_data


class UserDetailView(DetailView, PermissionRequiredMixin):
    model = User
    permission_required = "users.view_user"


class UserDeleteView(DeleteView, PermissionRequiredMixin, UserPassesTestMixin):
    model = User
    permission_required = "users.delete_user"
    login_url = "users:login"
    success_url = reverse_lazy("users:user_list")

    def test_func(self):
        return self.request.user.is_staff
