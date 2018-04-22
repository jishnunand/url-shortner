# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class UrlShortner(models.Model):
    """
    Django Model for storing URL
    """
    short_url = models.CharField(null=False, max_length=8, blank=False)
    long_url = models.TextField(null=False, blank=False)

    def __unicode__(self):
        return self.long_url
