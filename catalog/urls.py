from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.views import ProductsListView, ProductDetailView, ContactsView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView, \
    ProductsByCategoryView
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductsListView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('catalog/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('catalog/create/', ProductCreateView.as_view(), name='product_create'),
    path('catalog/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('catalog/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('articles/', ArticleListView.as_view(), name='articles_list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/update/', ArticleUpdateView.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('category/<int:category_id>/', ProductsByCategoryView.as_view(), name='products_by_category'),
]
