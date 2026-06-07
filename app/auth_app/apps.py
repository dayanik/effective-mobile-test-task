from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    name = 'auth_app'

    def ready(self):
        from auth_app.seed_db import init_rbac_models
        init_rbac_models()
