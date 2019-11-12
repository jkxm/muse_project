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
from location_options import *
# from location_dict import *
from django.views.decorators.csrf import csrf_exempt

# search view
LEVEL_CHOICES = (
    ('Internship', 'Internship'),
    ('Entry Level', 'Entry Level'),
    ('Mid Level', 'Mid Level'),
    ('Senior Level', 'Senior Level'),
)

CATEGORY_CHOICES = (
    ('Account Management','Account Management'),
    ('Business & Strategy','Business & Strategy'),
    ('Creative & Design','Creative & Design'),
    ('Customer Service','Customer Service'),
    ('Data Science','Data Science'),
    ('Editorial','Editorial'),
    ('Education','Education'),
    ('Engineering','Engineering'),
    ('Finance','Finance'),
    ('Fundraising & Development','Fundraising & Development'),
    ('Healthcare & Medicine','Healthcare & Medicine'),
    ('HR & Recruiting','HR & Recruiting'),
    ('Legal','Legal'),
    ('Marketing & PR','Marketing & PR'),
    ('Operations','Operations'),
    ('Project & Product Management','Project & Product Management'),
    ('Retail','Retail'),
    ('Sales','Sales'),
    ('Social Media & Community','Social Media & Community'),
)

def company_datalist_options():
    options_html = ""
    for c in Company.objects.all():
        options_html += "<option value="+str(c.id)+">"+c.name+"</option>"

    return options_html

def job_titles():
    options_html = ""
    s = set()
    for j in Job.objects.all():
        s.add(j.title)

    for title in s:
        options_html += '<option value="'+ title +'">' + title + '</option>'

    return options_html


def search(request):
    if request.method == "POST":
        levels = request.POST.getlist('levels')
        categories = request.POST.getlist('categories')
        # location and company sent as one input
        locations = request.POST.get('locations')
        companies = request.POST.get('companies')
        job_query = Job.objects.none()
        if request.POST.get('jobtitle'):
            job_query = Job.objects.filter(title__contains=request.POST.get('jobtitle'))
            return render(
                request,
                'index.html',
                {
                    'job_query': job_query,
                    'level_choices':LEVEL_CHOICES,
                    'category_choices':CATEGORY_CHOICES,
                    'company_choices':company_datalist_options(),
                    'location_options':location_options,
                    'job_titles':job_titles(),
                }
            )

        # fix filter to use OR not AND
        # use union operator on job query to include all jobs that have selected levels and categories
        for l in levels:
            job_query |= Job.objects.filter(level__contains=l)
        for c in categories:
            job_query |= Job.objects.filter(category__contains=c)


        # flexdatalist seperates values with __, so splitting string to get each company/location chosen
        companies_arr = companies.split("__")
        locations__arr = locations.split("__")

        # if there were no levels/ category selected, set job_query to all jobs
        if not job_query:
            job_query = Job.objects.all()

        if companies:
            for c in companies_arr:
                comp = Company.objects.get(name=c)
                job_query = job_query.filter(company = comp)

        for l in locations__arr:
            job_query = job_query.filter(location__contains=l)

        return render(
            request,
            'index.html',
            {
                'search_params':(levels, categories, locations, companies),
                'job_query':job_query,
                'level_choices':LEVEL_CHOICES,
                'category_choices':CATEGORY_CHOICES,
                'company_choices':company_datalist_options(),
                'location_options':location_options,
                'job_titles':job_titles(),
            }
        )
    return render(
        request,
        'index.html',
        {
            'level_choices':LEVEL_CHOICES,
            'category_choices':CATEGORY_CHOICES,
            'company_choices':company_datalist_options(),
            'location_options':location_options,
            'job_titles':job_titles(),
        }
    )


def job_post(request, job_id):
    job = Job.objects.get(id=job_id)
    return render(
        request,
        'job_post.html',
        {
            'job':job,
        }

    )

# API data consumption
@csrf_exempt
def api_to_db(request):

    if request.method == 'POST':
        # if file was provided
        if 'json_file' in request.FILES:
            json_file = request.FILES['json_file'].read()
            # f = open(json_file)
            data = json.loads(json_file)
            results = data["results"]
            for r in results:
                save_to_db(r)
            return render(
                request,
                'api_to_db.html',
                {
                    'message':results
                }
            )

        # if endpoint was provided
        else:
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

        if 'application/json' in ri['Content-Type']:
            data = response.read().decode('utf-8')
            output = json.loads(data)
            results = output["results"]
            for r in results:
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

    # save job if doesnt exist
    # but what if someone is publishing the same job again?
    # if not Job.objects.filter(title=title,  company=company, level=level, category=category, location=location, contents=contents).exists():
    job = Job(title=title, company=company, level=level, category=category, location=location, contents=contents)
    job.save()
