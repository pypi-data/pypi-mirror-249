from tempfile import TemporaryFile

from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.core.files.base import File
from django.core.files.storage import FileSystemStorage


class EncryptedFileStorage(FileSystemStorage):
    """
    Storage class for encrypted file fields.
    This uses the ENCRYPTED_FILES_KEY setting to encrypt/decrypt the contents
    of the files stored in the field.
    """

    def __init__(self, location=settings.SAFE_MEDIA_ROOT, *args, **kwargs):
        super().__init__(location=location, *args, **kwargs)
        self.fernet = Fernet(settings.ENCRYPTED_FILES_KEY)

    def save(self, name, content, *args, **kwargs):
        """Encrypt the contents of the original file and save it"""
        content.seek(0)
        content_bytes = content.read()
        encrypted = self.fernet.encrypt(content_bytes)
        temp_file = self.get_temp_file(encrypted)
        return super().save(name, temp_file, *args, **kwargs)

    def open(self, name, *args, **kwargs):
        """Read the contents of the saved file and decrypt it.
        The raw file will be returned if it fails.
        """
        fd = super().open(name, *args, **kwargs)
        fd.seek(0)
        try:
            decrypted = self.fernet.decrypt(fd.read())
        except InvalidToken:
            return fd
        temp_file = self.get_temp_file(decrypted)
        return File(temp_file)

    def get_temp_file(self, content):
        """Instantiate a temporary file with given content."""
        temp_file = TemporaryFile()
        temp_file.write(content)
        temp_file.seek(0)
        return temp_file
