from django.db import models

class Article(models.Model):
    title = models.CharField(
        max_length=300, verbose_name="Заголовок", help_text="Введите заголовок статьи"
    )
    content = models.TextField(
        verbose_name="Содержимое статьи",
        help_text="Введите содержимое статьи",
    )
    photo = models.ImageField(
        upload_to="blog/articles/",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите фото для статьи",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Укажите дату создания статьи",
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликовано",
        help_text="Отметьте для публикации статьи",
    )
    view_counter = models.PositiveIntegerField(
        verbose_name="Счетчик просмотров",
        default=0,
        editable=False,
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-created_at"]
        app_label = 'blog'

    def __str__(self):
        return f"{self.title} (Просмотров: {self.view_counter})"
