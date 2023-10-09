from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Tag(models.Model):
    name = models.CharField(null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Author(models.Model):
    fullname = models.CharField(unique=True)
    born_date = models.DateField()
    born_location = models.CharField()
    description = models.TextField(max_length=250)


    def __str__(self):
        return f"{self.fullname}"


class Quote(models.Model):
    quote = models.CharField(max_length=300, null=False, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
