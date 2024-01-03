from django.db import models

from encrypted_files.storage import EncryptedFileStorage


class EncryptedFileField(models.FileField):
    """
    A model FileField that encrypts the content on save and decrypt on reading.
    """

    def __init__(self, storage=None, *args, **kwargs):
        if not storage:
            storage = EncryptedFileStorage()
        super().__init__(storage=storage, *args, **kwargs)
