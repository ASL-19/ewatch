# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-23 17:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0008_auto_20170323_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='questioncategory',
            name='last_modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Last Modified Date'),
        ),
    ]
