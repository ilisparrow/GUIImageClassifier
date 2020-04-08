# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import dataProcessing

def DataProcessingView(request):
    context ={}
    page = dataProcessing(request.POST)
    
    return render(request, "dataProcessing.html",context)
