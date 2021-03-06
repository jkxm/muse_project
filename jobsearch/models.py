# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField
import collections

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    short_name = models.CharField(max_length=100, default="")
    def __unicode__(self):
        return self.name


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

# class Level(models.Model):
#
# class Category(models.Model):
#


class Job(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)

    company = models.ForeignKey('Company',null=False)

    # level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    level = JSONField(default=[], null=True, blank=True)
    category = JSONField(default=[], null=True, blank=True)
    location = JSONField(default=[], null=True, blank=True)

    # job category
    # what if more than one category?
    # delimit by character? arrayfield? json?
    # category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    contents = models.TextField(default="")

    def __unicode__(self):
        return self.title

    def show_levels(self):
        level_str = ""
        for l in self.level:
            level_str += l["name"] + ", "
        return level_str

    def show_locations(self):
        location_str = ""
        for l in self.location:
            location_str += l["name"] + ", "
        return location_str

    def show_categories(self):
        category_str = ""
        for c in self.category:
            category_str += c["name"] + ", "
        return category_str

    def content_snippet(self):
        return self.contents[:100]
