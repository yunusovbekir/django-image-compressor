from django.db import models


class ExampleModel(models.Model):
    title = models.CharField(max_length=255)
    image_1 = models.ImageField()
    image_2 = models.ImageField()
