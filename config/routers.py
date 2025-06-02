class CatalogRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'catalog':
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'catalog':
            return 'default'
        return None


class BlogRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'blog':
            return 'blog'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'blog':
            return 'blog'
        return None
