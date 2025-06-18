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

    def allow_migrate(self, db, app_label, **hints):
        # Запрещаем миграции для users в базе blog
        if app_label == 'users':
            return False
        if app_label == 'blog':
            return db == 'blog'
        return None


class UsersRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'users':
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'users':
            return 'default'
        return None

    def allow_migrate(self, db, app_label, **hints):
        if app_label == 'users':
            return db == 'default'
        return None


class SystemAppsRouter:
    def allow_migrate(self, db, app_label, **hints):
        system_apps = ['admin', 'auth', 'contenttypes', 'sessions']
        if app_label in system_apps:
            return db == 'default'
        return None