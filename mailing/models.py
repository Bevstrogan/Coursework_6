from django.db import models

from users.models import User


class Client(models.Model):
    email = models.EmailField(verbose_name="Почта", unique=True)
    full_name = models.CharField(max_length=100, verbose_name="ФИО")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Владелец", null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} : {self.email}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Message(models.Model):
    subject = models.CharField(max_length=50, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Владелец", null=True, blank=True)

    def __str__(self):
        return f"{self.subject}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Newsletter(models.Model):
    daily = "раз в день"
    weekly = "раз в неделю"
    monthly = "раз в месяц"
    Periodicity = [(daily, "раз в день"), (weekly, "раз в неделю"), (monthly, "раз в месяц")]

    finished = "завершена"
    created = "создана"
    launched = "запущена"
    Status = [(finished, "завершена"), (created, "создана"), (launched, "запущена")]

    start_time = models.DateTimeField(verbose_name="Время начала отправки рассылки")
    end_time = models.DateTimeField(verbose_name="Время окончания отправки рассылки")
    status = models.CharField(max_length=20, verbose_name="Статус рассылки", choices=Status, default=created)
    periodicity = models.CharField(max_length=20, verbose_name="Переодичность рассылки", choices=Periodicity)

    client = models.ManyToManyField(Client, verbose_name="Клиент", blank=True, null=True)
    message = models.ForeignKey(Message, verbose_name="Сообщение", on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Владелец", null=True, blank=True)

    def __str__(self):
        return f"Рассылка {self.start_time} - {self.end_time}, {self.status}, {self.periodicity}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ('change_status', 'Can change newsletters status'),
        ]


class Logs(models.Model):
    attempt = models.BooleanField(verbose_name="Статус попытки")
    attempt_time = models.DateTimeField(verbose_name="Дата и время последней операции")
    response = models.CharField(max_length=100, verbose_name="Ответ сервера", null=True, blank=True)

    client = models.ForeignKey(Client, on_delete=models.SET_NULL, verbose_name="Клиент", null=True)
    newsletter = models.ForeignKey(Newsletter, verbose_name="Рассылка", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Попытка от {self.attempt_time}, статус: {self.attempt}, ответ:{self.response}"

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = "Логи"
