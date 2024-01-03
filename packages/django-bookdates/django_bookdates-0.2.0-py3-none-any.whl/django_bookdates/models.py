import uuid

from django.urls import reverse
from django.db import models


class Calendar(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return f"{self.name} (/{self.slug})"


class Timespan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField()
    title = models.CharField(max_length=1024)
    body = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} (Calendar: {self.calendar.name})"

    def get_absolute_url(self):
        return reverse('listtimespans', kwargs={'calendar': self.calendar.slug })
