from django.db import models
from django.urls import reverse

# Create your models here.
class Todo(models.Model):
    body = models.CharField(max_length=400)
    due = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=(
            ("not-started", "Not started"),
            ("in-progress", "In progress"),
            ("completed", "Completed"),
        ),
        default="not-started",
    )

    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse("home")
