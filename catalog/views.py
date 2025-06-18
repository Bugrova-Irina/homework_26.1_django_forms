from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Product, Article


class ProductsListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductModeratorForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    permission_required = 'catalog.change_product'

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductModeratorForm

        if user.has_perm('catalog.can_unpublish_product'):
            return ProductForm
        raise PermissionDenied


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо, {name} ({phone})! Сообщение получено: {message}.")


class ArticleListView(ListView):
    model = Article
    template_name = 'catalog/articles_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(is_published=True)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'catalog/article_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_counter += 1
        self.object.save()
        return self.object


class ArticleCreateView(CreateView, LoginRequiredMixin):
    model = Article
    fields = ('title', 'content', 'photo', 'is_published')
    template_name = 'catalog/article_form.html'
    success_url = reverse_lazy('catalog:articles_list')


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ('title', 'content', 'photo', 'is_published')
    template_name = 'catalog/article_form.html'
    success_url = reverse_lazy('catalog:articles_list')

    def get_success_url(self):
        return reverse('catalog:article_detail', args=[self.kwargs.get('pk')])


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'catalog/article_confirm_delete.html'
    success_url = reverse_lazy('catalog:articles_list')