# Django Image Compressor

Django Image Compressor is a tool to compress your images. Easy to plug-in and easy to use.
The tool compresses the uploaded image before saving data to db.

### Installation

To install django-image-compressor
```sh
$ pip install django-image-compressor
```

Add the app to your project:
```py
# settings.py
INSTALLED_APPS = (
    ...
    'django-image-compressor',
    ...
)
```

### Usage

Package will add additional 4 fields to your forms. You can compress your images by reducing the quality of the images or resize them or both. If you leave input width and/or height fields empty and try to resize your image, sizes will be reduced twice. Only compressed images will be saved to your db and original ones will be ignored.

In order to use the compressor, first create a ModelForm in forms.py and add ImageCompressorFormMixin to your form:

```py
# forms.py
from django import forms
from django_image_compressor.mixins import ImageCompressorFormMixin

class YourImageUploadForm(ImageCompressorFormMixin, forms.ModelForm):
    ...
    compressed_image_fields = ('your_image_field_1', 'your_image_field2', ...)
    ...

```


If you want to add compressor to your Django Admin Site, then add ImageCompressorAdminMixin and the created form to your ModelAdmin class.

```py
# admin.py
from django.contrib import admin
from django_image_compressor.mixins import ImageCompressorAdminMixin
from .forms.py import YourImageUploadForm

class YourModelAdmin(ImageCompressorAdminMixin, admin.ModelAdmin):
    ...
    custom_form = YourImageUploadForm
    ...

```
