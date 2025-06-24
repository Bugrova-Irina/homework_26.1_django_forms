from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Product, Article, Category
from catalog.services import get_products_by_category


class ProductsListView(ListView):
    """ Класс для отображения списка продуктов """
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        """Добавляем категории в контекст"""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('name')
        return context

    def get_queryset(self):
        # получаем закешированные данные по ключу my_queryset
        queryset = cache.get('my_queryset')
        # если в кеш ничего нет
        if not queryset:
            queryset = super().get_queryset() # выполняем запрос к базе данных
            cache.set('my_queryset', queryset, 60 * 15) # кешируем данные на 15 минут
        return queryset


class ProductsByCategoryView(ListView):
    """Класс для отображения товаров по категории"""
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        """Возвращает товары для указанной категории"""
        category_id = self.kwargs['category_id']
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        """Добавляем информацию о категории в контекст"""
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['category_id']
        context['category'] = get_object_or_404(Category, id=category_id)
        return context


class ProductDetailView(DetailView):
    """ Класс для отображения деталей продукта """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView, LoginRequiredMixin):
    """ Класс для создания продукта """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        # автоматическое назначение владельцем продукта пользователя, создавшего продукт
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Класс для редактирования продукта """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    permission_required = 'catalog.change_product'

    def get_form_class(self):
        user = self.request.user
        # если авторизован владелец продукта и он не модератор, загружается форма ProductForm
        if user == self.object.owner and not user.has_perm('catalog.can_unpublish_product'):
            return ProductForm

        # если авторизован модератор, загружается форма ProductModeratorForm
        if user.has_perm('catalog.can_unpublish_product'):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """ Класс для удаления продукта """
    model = Product
    success_url = reverse_lazy('catalog:home')

    def get_object(self, queryset=None):
        """ Возвращает объект для удаления с предварительной проверкой прав """
        obj = super().get_object(queryset)
        user = self.request.user

        # проверяем, что пользователь является модератором
        has_unpublish_permission = user.has_perm('catalog.can_unpublish_product')

        # проверяем владение продуктом
        is_owner = obj.owner == user

        if not (has_unpublish_permission or is_owner):
            raise PermissionDenied("У вас нет прав для удаления этого продукта")

        return obj


class ContactsView(TemplateView):
    """ Класс для отображения формы обратной связи """
    template_name = 'catalog/contacts.html'

    def get(self, request, *args, **kwargs):
        # обработка get-запроса, рендеринг шаблона формы
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # обработка Post-запроса, отправка сообщения от пользователя
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо, {name} ({phone})! Сообщение получено: {message}.")


class ArticleListView(ListView):
    """ Класс для отображения списка статей """
    model = Article
    template_name = 'catalog/articles_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        # отображение только опубликованных статей
        return Article.objects.filter(is_published=True)


class ArticleDetailView(DetailView):
    """ Класс для отображения деталей статьи """
    model = Article
    template_name = 'catalog/article_detail.html'

    def get_object(self, queryset=None):
        # счетчик просмотров статьи
        self.object = super().get_object(queryset)
        self.object.view_counter += 1
        self.object.save()
        return self.object


class ArticleCreateView(CreateView, LoginRequiredMixin):
    """ Класс для создания статьи """
    model = Article
    fields = ('title', 'content', 'photo', 'is_published')
    template_name = 'catalog/article_form.html'
    success_url = reverse_lazy('catalog:articles_list')


class ArticleUpdateView(UpdateView):
    """ Класс для редактирования статьи """
    model = Article
    fields = ('title', 'content', 'photo', 'is_published')
    template_name = 'catalog/article_form.html'
    success_url = reverse_lazy('catalog:articles_list')

    def get_success_url(self):
        return reverse('catalog:article_detail', args=[self.kwargs.get('pk')])


class ArticleDeleteView(DeleteView):
    """ Класс для удаления статьи """
    model = Article
    template_name = 'catalog/article_confirm_delete.html'
    success_url = reverse_lazy('catalog:articles_list')

