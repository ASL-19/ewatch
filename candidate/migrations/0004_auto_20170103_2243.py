# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-03 22:43
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0003_auto_20161229_2002'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='party',
            options={'verbose_name_plural': 'Political Parties'},
        ),
        migrations.AlterField(
            model_name='candidate',
            name='political_background',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Political Background'),
        ),
    ]