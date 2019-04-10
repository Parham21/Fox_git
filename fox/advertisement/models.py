import os

from django.contrib.auth.models import User
from django.db import models

from advertisement.constant import SEX_CHOICES


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)

class Advertisement(models.Model):
    title = models.CharField(max_length=80)
    price = models.IntegerField()
    phone = models.CharField(max_length=12)
    description = models.TextField()
    profile_image = models.ImageField(upload_to=get_image_path, default='photos/default.jpg', null=True)


    area = models.ForeignKey('Area', on_delete=models.CASCADE)
    advertiser = models.ForeignKey('Advertiser', on_delete=models.CASCADE)


    def __str__(self):
        return self.title + ' ' + self.area.name + ' ' + self.area.city.name

class Advertiser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=12)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    age = models.IntegerField()

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class City(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=40)

    city = models.ForeignKey('City', on_delete=models.CASCADE)

    def __str__(self):
        return self.city.name + ' ' + self.name