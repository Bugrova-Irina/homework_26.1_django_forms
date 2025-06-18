from django import forms
from django.core.exceptions import ValidationError
from django.forms import BooleanField

from catalog.models import Product


FORBIDDEN_WORDS = [
    'казино',
    'криптовалюта',
    'крипта',
    'биржа',
    'дешево',
    'бесплатно',
    'обман',
    'полиция',
    'радар',
]

class StyleFormMixin: # Класс-миксин для стилизации полей формы создания/редактирования товара
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProductForm, self).__init__(*args, **kwargs)

        # скрываем поле is_published, если у пользователя нет прав
        if self.user and not self.user.has_perm('catalog.can_unpublish_product'):
            self.fields.pop('is_published', None)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Укажите название товара',
        })

        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Добавьте описание товара',
        })

        self.fields['photo'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['category'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Укажите категорию товара',
        })

        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Укажите цену товара'
        })

    def clean_name(self): # Проверка на наличие запрещенных слов в названии товара
        cleaned_data = super().clean()
        product_name = cleaned_data.get('name', '').lower()
        for word in FORBIDDEN_WORDS:
            if word in product_name:
                raise ValidationError(f'Использование слова "{word}" запрещено.')

        return product_name

    def clean_description(self): # Проверка на наличие запрещенных слов в описании товара
        cleaned_data = super().clean()
        product_description = cleaned_data.get('description', '').lower()
        for word in FORBIDDEN_WORDS:
            if word in product_description:
                raise ValidationError(f'Использование слова "{word}" запрещено.')

        return product_description

    def clean_price(self): # Проверка на то, что цена товара > 0
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError('Цена товара не может быть меньше нуля.')
        return price
