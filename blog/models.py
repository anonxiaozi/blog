from django.db import models
from mdeditor.fields import MDTextField


# Create your models here.


class User(models.Model):
    user_name = models.CharField(max_length=50, unique=True)
    register_time = models.DateTimeField(auto_now_add=True)

    class META:
        ordering = ['-register_time']

    def __str__(self):
        return self.user_name


class Blog(models.Model):
    title = models.CharField(max_length=50)
    label = models.ForeignKey('Label', on_delete=models.SET_DEFAULT, default=0)
    summary = models.CharField(max_length=50)
    background_img = models.ForeignKey('Image', on_delete=models.SET_NULL, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    content = MDTextField()
    user = models.ForeignKey('User', on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.title


class Label(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='background_img', max_length=10240)

    def __str__(self):
        return self.image.name

