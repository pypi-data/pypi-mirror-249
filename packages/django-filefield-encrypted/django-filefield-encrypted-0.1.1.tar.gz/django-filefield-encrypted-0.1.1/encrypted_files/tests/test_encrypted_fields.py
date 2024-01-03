import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import connection
from django.test import RequestFactory, TestCase

from encrypted_files.tests.test_models.models import TestModel
from encrypted_files.views import EncryptedFileDetailView


class EncryptedFieldsTestCase(TestCase):
    content = b"abc"
    upload = SimpleUploadedFile("foo.txt", content, content_type="text/txt")

    def setUp(self):
        sql = (
            'CREATE TABLE "encrypted_filefield_test_models_testmodel" '
            '("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, '
            '"document" varchar(100) NOT NULL);'
        )
        cursor = connection.cursor()
        cursor.execute(sql)

        self.obj = TestModel.objects.create(document=self.upload)

    def test_create_model(self):
        """Assert the file is encrypted and saved in the right place"""
        # file is stored in the safe vault
        self.assertTrue(self.obj.document.path.startswith(settings.SAFE_MEDIA_ROOT))
        self.assertTrue(os.path.isfile(self.obj.document.path))

        # content can be read unencrypted
        with self.obj.document.open() as f:
            self.assertEqual(f.read(), self.content)

        # plain content is encrypted
        with open(self.obj.document.path, "rb") as f:
            self.assertNotEqual(f.read(), self.content)

    def test_view_document_content(self):
        """Subclass the file view and assert it returns the plain content"""

        class TestingView(EncryptedFileDetailView):
            model = TestModel
            encrypted_file_field = "document"

        factory = RequestFactory()
        request = factory.get("")
        response = TestingView.as_view()(request, pk=self.obj.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.content, response.content)
