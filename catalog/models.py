from django.db import models

class Category(models.Model):
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

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name', 'category', 'price']
        app_label = 'catalog'

    def __str__(self):
        return self.name
