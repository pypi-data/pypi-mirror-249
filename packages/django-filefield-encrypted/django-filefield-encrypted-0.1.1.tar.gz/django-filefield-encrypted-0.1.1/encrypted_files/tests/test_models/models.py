from django.db import models

from encrypted_files.fields import EncryptedFileField


class TestModel(models.Model):
    document = EncryptedFileField(upload_to="testing/")

    class Meta:
        app_label = "encrypted_filefield_test_models"
