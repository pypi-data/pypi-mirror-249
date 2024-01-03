import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django-filefield-encrypted",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    license="GNU License",
    description="Encryted file field for Django",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/gsteixeira/django-filefield-encrypted",
    author="Gustavo Selbach Teixeira",
    author_email="gsteixei@gmail.com",
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
    ],
    requirements=[
        "django",
        "cryptography",
    ],
)
