# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-08 19:24
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobsearch', '0003_auto_20191108_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='category',
            field=jsonfield.fields.JSONField(blank=True, default=[], null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='level',
            field=jsonfield.fields.JSONField(blank=True, default=[], null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='location',
            field=jsonfield.fields.JSONField(blank=True, default=[], null=True),
        ),
    ]
