import tempfile
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from PIL import Image


DIR = os.path.join(settings.BASE_DIR, 'tmp_folder')


def create_example_image(title, width, height):
    import pdb

    image = Image.new('RGB', (width, height))
    tmp_img = tempfile.NamedTemporaryFile(suffix='.jpg')
    title = os.path.join(DIR, title)
    pdb.set_trace()

    image.save(title, tmp_img)
    temp_image = open(title, 'rb')

    created_image = SimpleUploadedFile(
        name=title,
        content=temp_image.read(),
    )
    return created_image


class TestImageCompression(TestCase):

    def setUp(self):
        image_1 = create_example_image('image_1.jpg', 1000, 1000)
        image_2 = create_example_image('image_2.jpg', 2000, 2000)
        self.data = {
            'title': 'Example data',
            'image_1': image_1,
            'image_2': image_2,
        }

    def test_create_instance_without_image_compression(self):
        """
        If appropriate fields are None, image compression should be ignored.
        """

        client = Client()
        response = client.post(
            path=reverse('create_view'),
            data=self.data,
        )
        print(response.data)
        self.assertEqual(response.status_code, 200)
