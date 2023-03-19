from django.db import models
from django.urls import reverse

# Create your models here.
class Todo(models.Model):
    body = models.CharField(max_length=400)
    due = models.DateField()

    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse("home")
