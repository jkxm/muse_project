# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse
# from rest_framework.parsers import JSONParsers
from jobsearch.models import *
from jobsearch.serializers import *
from django.shortcuts import render
from urllib2 import urlopen
import urllib2
import json
from django.views.decorators.csrf import csrf_exempt

# search view
def search(request):
    return render(
        request,
        'index.html',
    )

# API data consumption
@csrf_exempt
def api_to_db(request):

    if request.method == 'POST':
        url = request.POST.get('api_endpoint')
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'
        }
        req = urllib2.Request(url, headers=hdr)

        try:
            response = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.fp.read()

        ri = response.info()
        # if responseself.
        if 'application/json' in ri['Content-Type']:
            # ri = "checked header"
            data = response.read().decode('utf-8')
            output = json.loads(data)
            results = output["results"]
            for r in output["results"]:
                save_to_db(r)
            # results = response.read()


        return render(
            request,
            'api_to_db.html',
            {
                'message':results
            }
        )

    return render(
        request,
        'api_to_db.html',
        {
            # 'message':output
        }
    )


# save to debug
def save_to_db(json_obj):
    title = json_obj["name"]
    # Company
    level = json_obj["levels"]
    category = json_obj["categories"]
    location = json_obj["locations"]

    # job desc
    contents = json_obj["contents"]

    # company fields
    company_obj = json_obj.get('company', None)
    company_name = company_obj['name']
    company_id = company_obj['id']
    company_shortname = company_obj['short_name']
    # check if company exists, if not, make one

    company = None
    if Company.objects.filter(id=company_id, name=company_name).exists():
        company = Company.objects.get(id=company_id, name=company_name)
    else:
        company = Company(id=company_id, name=company_name, short_name=company_shortname)
        company.save()

    job = Job(title=title, company=company, level=level, category=category, location=location, contents=contents)
    job.save()
