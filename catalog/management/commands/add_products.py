from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category

class Command(BaseCommand):
    help = 'Load test products from fixtures'

    def handle(self, *args, **kwargs):
        # Удаляем существующие записи
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Загрузка данных из фикстур
        call_command('loaddata', 'categories.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
        call_command('loaddata', 'products.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
