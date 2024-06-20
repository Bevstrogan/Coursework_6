from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import Homepage, ClientCreateView, ClientListView, ClientDetailView, ClientUpdateView, \
    ClientDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path("", Homepage.as_view(), name="home"),
    path("client_list/", ClientListView.as_view(), name="client_list"),
    path("create_client/", ClientCreateView.as_view(), name="create_client"),
    path("view_client/<int:pk>", ClientDetailView.as_view(), name="view_client"),
    path("edit_client/<int:pk>", ClientUpdateView.as_view(), name="edit_client"),
    path("delete_client/<int:pk>", ClientDeleteView.as_view(), name="delete_client"),
]