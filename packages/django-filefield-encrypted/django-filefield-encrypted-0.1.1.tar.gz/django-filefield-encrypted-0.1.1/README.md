DJANGO FILE FIELD ENCRYPTED
---------------------------

django-filefield-encrypted - An encrypted file field for Django.

This will encrypt when saving and decrypt on reading files on the fly.
Files will be stored in a directory other than MEDIA_ROOT, so not exposed through 'media/...'.


INSTALLATION
------------

Install django-filefield-encrypted:

.. code:: shell

    pip install django-filefield-encrypted

Then add to your settings.py:

.. code:: python

    # the key to encrypt the files. Keep it safe!
    ENCRYPTED_FILES_KEY = b"<your key here>"
    # The directory where files will be stored.
    SAFE_MEDIA_ROOT = BASE_DIR / "safe/"

You can generate a key with:

.. code:: python

    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    print(key)


USAGE
-----

In your models.py:


.. code:: python

        from encrypted_files.fields import EncryptedFileField

        class Foobar(models.Model):
            foo = EncryptedFileField(upload_to="whatever/")


You can create your records normally. To read the file contents:

.. code:: python

        from encrypted_files.fields import EncryptedFileField

        obj = Foobar.objects.get(pk=pk)
        with obj.foo.open(mode="rb") as f:
            content = f.read()


To retrieve the contents of the file in a view:

.. code:: python

        from encrypted_files.views import EncryptedFileDetailView

        class FoobarView(EncryptedFileDetailView):
            model = Foobar
            encrypted_file_field = "foo"


Add this view to your urls.py. When you go to that url it will return the plain contents of the file. Treat if like a ´django.views.generic.detail.DetailView´.
All you need is to indicate the model and the ´encrypted_file_field´ which is the field that contains the encrypted file.
So let's say you want to store an image, and use it in your html. Given the above example. This is how the template would look like:

.. code:: html

        <img src="{% url 'foo_view_url_name' object.pk %}" />

That's it! The rendering page will load the image from that url, that will return the contents of the encrypted file transparently.


Alternatively you can also use it to download the file, in your template add the download link:

.. code:: html

        <a href="{% url 'foo_view_url_name' object.pk %}" download>
            click here...
        </a>

