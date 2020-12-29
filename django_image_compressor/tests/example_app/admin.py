from django.contrib import admin
from django_image_compressor.mixins import ImageCompressionAdminMixin
from .models import ExampleModel


class ExampleAdmin(ImageCompressionAdminMixin, admin.ModelAdmin):
    compressed_image_fields = ('image_1', 'image_2')


admin.site.register(ExampleModel)
