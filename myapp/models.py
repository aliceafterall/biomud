from __future__ import unicode_literals

from django.db import models

# Create your models here.

class A(models.Model):
    _DATABASE = "myapp"
    title = models.CharField(max_length=200)
