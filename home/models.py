# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Cameras(models.Model):
    done = models.BooleanField(default=False) 
    name = models.CharField(max_length = 200)   
# Create your models here.
