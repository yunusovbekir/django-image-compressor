from django.db import models


class ExampleModel(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField()
    image_2 = models.ImageField()

    class Meta:
        app_label = 'test_app'
