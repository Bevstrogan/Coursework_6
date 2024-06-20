from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=15, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Содержимое статьи", null=True, blank=True)
    image = models.ImageField(upload_to="blog/", verbose_name="Изображение", blank=True, null=True)
    views_count = models.IntegerField(default=0, verbose_name="Количество просмотров")
    published_date = models.DateTimeField(verbose_name="Дата публикации", auto_now_add=True)

    def __str__(self):
        return f"Название блога: {self.title}"

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"
