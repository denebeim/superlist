from django.core.exceptions import ValidationError
from django.db import models


class List(models.Model):
    pass


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=None, default=None)

    def clean(self):
        if self.text == '':
            raise ValidationError("You can't have an empty list item")
