from django.db import models

# Create your models here.

class Post(models.Model):
    user = models.CharField(max_length=100)
    post = models.CharField(max_length=140)
    data = models.CharField(max_length=50)
    imagem = models.CharField(max_length=200)

class User(models.Model):
    user = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)
    imagem = models.FileField(null=True, blank=False)