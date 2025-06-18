from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Product, Article


class ProductsListView(ListView):
    """ Класс для отображения списка продуктов """
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


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


class ProductDeleteView(DeleteView):
    """ Класс для удаления продукта """
    model = Product
    success_url = reverse_lazy('catalog:home')


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
