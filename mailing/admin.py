from django.contrib import admin

from mailing.models import Client, Message, Newsletter, Logs


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display =("full_name", "email",)
    search_fields = ("full_name",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "body",)
    search_fields = ("body",)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("status", "periodicity",)
    list_filter = ("status", "periodicity",)


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ("attempt", "attempt_time", "response",)
    search_fields = ("client", "newsletter",)
