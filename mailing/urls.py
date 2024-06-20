from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import Homepage, ClientCreateView, ClientListView, ClientDetailView, ClientUpdateView, \
    ClientDeleteView, MessageListView, MessageCreateView, MessageDetailView, MessageUpdateView, MessageDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path("", Homepage.as_view(), name="home"),
    path("client_list/", ClientListView.as_view(), name="client_list"),
    path("create_client/", ClientCreateView.as_view(), name="create_client"),
    path("view_client/<int:pk>", ClientDetailView.as_view(), name="view_client"),
    path("edit_client/<int:pk>", ClientUpdateView.as_view(), name="edit_client"),
    path("delete_client/<int:pk>", ClientDeleteView.as_view(), name="delete_client"),

    path("message/list", MessageListView.as_view(), name="list_message"),
    path("message/create", MessageCreateView.as_view(), name="create_message"),
    path("message/view/<int:pk>", MessageDetailView.as_view(), name="view_message"),
    path("message/edit/<int:pk>", MessageUpdateView.as_view(), name="edit_message"),
    path("message/delete/<int:pk>", MessageDeleteView.as_view(), name="delete_message"),
]