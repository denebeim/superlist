from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class List(models.Model):
    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=None, default=None)

    def __str__(self):
        return self.text

    def clean(self):
        if self.text == '':
            raise ValidationError("You can't have an empty list item")

    class Meta:
        unique_together = ('list', 'text')
        ordering = ('id',)
