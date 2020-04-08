# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class dataProcessing(models.Model):
    title = models.CharField(max_length = 200)   
    # renames the instances of the model 
    # with their title name 
    def __str__(self): 
        return self.title 
