from django.forms import ModelForm

from mailing.models import Client, Message, Newsletter


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ("full_name", "email", "comment",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = 'form-control'


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ("subject", "body",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = 'form-control'


class NewsletterForm(MessageForm):
    class Meta:
        model = Newsletter
        fields = ("start_time", "end_time", "status", "periodicity", "client", "message")
