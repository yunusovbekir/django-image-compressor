import os
import logging

from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.translation import gettext_lazy as _
from PIL import Image

from .utils import create_tmp_dir, remove_tmp_dir

logger = logging.getLogger(__name__)


class ImageCompressorFormMixin:
    compressed_image_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_list = [key for key in self.fields.keys()]

        for field in self.compressed_image_fields:

            reduce_memory_checkbox_field = 'reduce_memory_%s' % field
            resize_checkbox_field = 'resize_%s' % field
            width_input_field = 'width_%s' % field
            height_input_field = 'height_%s' % field

            self.fields[reduce_memory_checkbox_field] = forms.BooleanField(
                required=False,
                label=_('%s reduce memory' % field),
                help_text=_('It will reduce only the memory of the image'),
            )
            self.fields[resize_checkbox_field] = forms.BooleanField(
                required=False,
                label=_('%s resize' % field),
                help_text=_(
                    'It will reduce both the memory and the size of the image'
                ),
            )
            self.fields[width_input_field] = forms.IntegerField(
                required=False,
                label=_('%s width' % field),
                min_value=1,
                help_text=_(
                    'Set custom width. '
                    'If custom width is not defined, it will be reduced twice'
                ),
            )
            self.fields[height_input_field] = forms.IntegerField(
                required=False,
                label=_('%s height' % field),
                min_value=1,
                help_text=_(
                    'Set custom height. '
                    'If custom height is not defined, it will be reduced twice'
                ),
            )

            # reordering fields
            additional_fields_list = [
                reduce_memory_checkbox_field,
                resize_checkbox_field,
                width_input_field,
                height_input_field,
            ]

            index_field = fields_list.index(field)
            index_field += 1
            reordered_list = fields_list[:index_field] + additional_fields_list + fields_list[index_field:]

            self.fields = {k: self.fields[k] for k in reordered_list}

    def clean(self):
        cleaned_data = super().clean()
        if self.compressed_image_fields:
            temp_folder = create_tmp_dir()

            for field in self.compressed_image_fields:
                if cleaned_data.get(field):
                    self.start_compression(cleaned_data, temp_folder, field)

            remove_tmp_dir(temp_folder)

        return cleaned_data

    def start_compression(self, data, temp_folder, field):

        # get `reduce memory` and `resize` field names
        reduce_memory_field = 'reduce_memory_%s' % field
        resize_field = 'resize_%s' % field

        # get field data
        reduce_memory = data.get(reduce_memory_field)
        resize = data.get(resize_field)

        # if user wants to compress, proceed...
        if reduce_memory or resize:
            logger.info(_(
                'Image [%s] compression is started...' % field
            ))

            quality = 'quality_%s' % field
            width = 'width_%s' % field
            height = 'height_%s' % field

            file_details = {
                'quality': data.get(quality),
                'width': data.get(width),
                'height': data.get(height)
            }

            self.compress_image(
                data, field, resize, temp_folder, **file_details
            )

    def compress_image(self, data, field, resize, temp_folder, **kwargs):

        uploaded_image = data.get(field)
        image = Image.open(uploaded_image)

        # if input quality data is not provided set 20 by default
        quality = kwargs.get('quality') if kwargs.get('quality') else 20

        if resize:
            params = {
                'image_obj': image,
                'input_width': kwargs.get('width'),
                'input_height': kwargs.get('height'),
                'quality': quality,
            }
            quality, image = self.resize_image(**params)

        logger.info(_('Image quality has been set to %s' % quality))

        # image file path
        temp_image_path = os.path.join(temp_folder, uploaded_image.name)

        # save image to the path
        image.save(temp_image_path, quality=quality, optimize=True)

        # get saved image
        temp_image = open(temp_image_path, 'rb')

        # wrap bytes file with UploadedFile object
        compressed_image = SimpleUploadedFile(
            name=uploaded_image.name,
            content=temp_image.read(),
            content_type=uploaded_image.content_type
        )
        data[field] = compressed_image
        logger.info(_('Image [%s] compression is completed.' % field))

    def resize_image(self, **kwargs):

        image = kwargs.get('image_obj')
        width = kwargs.get('input_width')
        height = kwargs.get('input_height')
        quality = kwargs.get('quality')

        original_width, original_height = image.size

        # if input size is not defined, reduce size twice.
        # if input size is greater than original size, ignore input size.
        width = self.set_size('width', width, original_width)
        height = self.set_size('height', height, original_height)

        # resize and assign to the variable
        image = image.resize((width, height), Image.ANTIALIAS)

        # since reducing size affects to the quality of the image
        # we change the new quality from 20 to 70
        quality = 70 if quality == 20 else quality
        logger.info(_(
            'Image width and height have been set to {} and {}'.format(
                width, height
            )))

        return quality, image

    def set_size(self, size, input_size, original_size):
        import math

        if input_size:
            input_size = int(input_size)

        if not input_size or input_size > original_size:
            logger.warning(_(
                'Input {size} either is not defined '
                'or is greater than original {size}.'
                'Value is ignored.'.format(size=size)
            ))
            input_size = math.floor(original_size / 2)

        return input_size


class ImageCompressionAdminMixin:
    custom_form = None

    def get_form(self, request, obj=None, change=False, **kwargs):
        if self.custom_form:
            return self.custom_form
        else:
            return super().get_form(request, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if self.fieldsets:
            return self.fieldsets
        elif self.custom_form:
            fieldsets = (
                (None, {
                    'fields': [k for k in self.custom_form().fields.keys()]
                }),
            )
            return fieldsets
        else:
            return super().get_fieldsets(request, obj)
