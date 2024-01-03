import mimetypes

from django.http import HttpResponse
from django.views.generic.detail import DetailView


class EncryptedFileDetailView(DetailView):
    """
    This view exposes the content of the encrypted file. From the field
    given by 'encrypted_file_field' of the model given by 'model'.
    """

    def render_to_response(self, request, *args, **kwargs):
        file_field = getattr(self.get_object(), self.encrypted_file_field)

        with file_field.open(mode="rb") as f:
            content = f.read()

        if not content:
            content = ""

        content_type = mimetypes.guess_type(file_field.path)[0]
        return HttpResponse(content, content_type=content_type)
