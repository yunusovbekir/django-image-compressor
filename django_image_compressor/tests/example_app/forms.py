from django import forms
from django_image_compressor.mixins import ImageCompressorFormMixin
from .models import ExampleModel


class ExampleForm(ImageCompressorFormMixin, forms.ModelForm):
    compressed_image_fields = ('image_1', 'image_2')

    class Meta:
        model = ExampleModel
        fields = '__all__'
