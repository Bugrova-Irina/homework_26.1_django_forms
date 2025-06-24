from django.core.cache import cache

from catalog.models import Product
from config.settings import CACHE_ENABLED


def get_products_by_category(category_id):
    """
    Возвращает список всех продуктов из выбранной категории из кеша,
    если кеш пуст, получает данные из БД
    """
    if not CACHE_ENABLED:
        # Если кеширование отключено, возвращаем данные напрямую из БД
        return list(
            Product.objects.filter(category_id=category_id).select_related('category')
        )

    # задаем уникальный ключ для категории
    key = f'products_by_category_{category_id}'

    # Получаем данные из кеша
    products = cache.get(key)

    if products is not None:
        return products

    # Если кеш пустой, получаем данные из БД
    products = list(
        Product.objects.filter(category_id=category_id).select_related('category')
    )

    # Сохраняем в кеш с таймаутом 15 минут
    cache.set(key, products, timeout=60 * 15)

    return products
