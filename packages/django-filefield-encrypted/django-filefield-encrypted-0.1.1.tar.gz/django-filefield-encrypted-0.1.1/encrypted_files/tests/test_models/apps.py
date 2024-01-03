from django.apps import AppConfig


class TestModelsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "encrypted_files.tests.test_models"
    label = "encrypted_filefield_test_models"
