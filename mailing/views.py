from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView, DeleteView

from mailing.forms import ClientForm, MessageForm, NewsletterForm
from mailing.models import Client, Message, Newsletter


class Homepage(TemplateView):
    template_name = "mailing/base.html"


class ClientCreateView(CreateView, LoginRequiredMixin):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")
    login_url = 'users:login'

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientListView(ListView, LoginRequiredMixin):
    model = Client
    success_url = reverse_lazy("mailing:client_list")
    login_url = 'users:login'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.kwargs.get('pk'))
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['clients_list'] = Client.objects.all()
        return context_data


class ClientUpdateView(UpdateView, LoginRequiredMixin):
    model = Client
    fields = ("full_name", "email", "comment",)
    success_url = reverse_lazy("mailing:client_list")
    login_url = "users:login"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner == self.request.user or self.request.user.is_superuser:
            return self.object
        else:
            return Http404


class ClientDetailView(DetailView, LoginRequiredMixin):
    model = Client
    login_url = "users:login"


class ClientDeleteView(DeleteView, LoginRequiredMixin):
    model = Client
    success_url = reverse_lazy("mailing:client_list")
    login_url = "users:login"


class MessageCreateView(LoginRequiredMixin,CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:list_message")
    login_url = "users:login"

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class MessageUpdateView(UpdateView, LoginRequiredMixin):
    model = Message
    fields = ("subject", "body",)
    success_url = reverse_lazy("mailing:list_message")
    login_url = "users:login"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object


class MessageListView(ListView, LoginRequiredMixin):
    model = Message
    success_url = reverse_lazy("mailing:list_message")
    login_url = "users:login"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data["message_list"] = Message.objects.all()
        return context_data


class MessageDetailView(DetailView):
    model = Message


class MessageDeleteView(DeleteView, LoginRequiredMixin):
    model = Message
    success_url = reverse_lazy("mailing:list_message")
    login_url = "users:login"


class NewsletterCreateView(CreateView, LoginRequiredMixin):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("mailing:list_newsletter")
    login_url = "users:login"

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class NewsletterUpdateView(UpdateView, LoginRequiredMixin):
    model = Newsletter
    fields = ("start_time", "end_time", "periodicity", "status", "client", "message")
    success_url = reverse_lazy("mailing:list_newsletter")
    login_url = "users:login"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner == self.request.user or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404


class NewsletterListView(ListView, LoginRequiredMixin):
    model = Newsletter
    success_url = reverse_lazy("mailing:list_newsletter")
    login_url = "users:login"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data["newsletter_list"] = Newsletter.objects.all()
        unique_clients = Client.objects.all().count()
        context_data["clients"] = unique_clients
        return context_data

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.kwargs.get('pk'))
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class NewsletterDetailView(DetailView):
    model = Newsletter

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.kwargs.get("pk"))
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class NewsletterDeleteView(DeleteView, LoginRequiredMixin):
    model = Newsletter
    success_url = reverse_lazy("mailing:list_newsletter")
    login_url = 'users:login'
