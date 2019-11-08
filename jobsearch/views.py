# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParsers
from jobsearch.models import *
from jobsearch.serializers import *
from django.shortcuts import render

# search view
def search(request):
    return render(
        request,
        'index.html',
    )

# API data consumption
def api_to_db(request):

    return render(
        request,
        'api_to_db.html',

    )
