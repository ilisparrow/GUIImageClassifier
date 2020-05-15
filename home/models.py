# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Cameras(models.Model):
    name = models.CharField(max_length = 200)   
    ip = models.CharField(max_length = 200)   
    done = False 
# Create your models here.
