from django.db import models

from users.models import User


class Category(models.Model):
    """ Модель категории продукта """
    name = models.CharField(
        max_length=200,
        verbose_name='Название категории',
        help_text='Введите название категории',
    )
    description = models.TextField(
        verbose_name='Описание категории',
        help_text='Введите описание категории',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
        app_label = 'catalog'

    def __str__(self):
        return self.name


class Product(models.Model):
    """ Модель продукта """
    name = models.CharField(
        max_length=250,
        verbose_name='Название товара',
    )
    description = models.TextField(
        verbose_name='Описание товара',
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        upload_to='catalog/image',
        blank=True,
        null=True,
        verbose_name='Изображение товара',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        blank=True,
        null=True,
        related_name='products',
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Цена',
    )
    in_stock = models.BooleanField(
        default=False,
        verbose_name='Наличие товара',
        help_text='Отметьте, если товар есть в наличии'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания карточки товара',
        help_text='Указывается дата и время создания товара',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления карточки товара',
        help_text='Указывается дата и время обновления данных о товаре',
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликовано',
        help_text='Отметьте для публикации товара',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='Владелец',
        help_text='Укажите владельца продукта',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name', 'category', 'price']
        app_label = 'catalog'
        # добавление кастомного права
        permissions = [
            ('can_unpublish_product', 'Can unpublish product'),
        ]

    def __str__(self):
        return self.name


class Article(models.Model):
    """ Модель статьи """
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
        app_label = 'catalog'

    def __str__(self):
        return f"{self.title} (Просмотров: {self.view_counter})"
