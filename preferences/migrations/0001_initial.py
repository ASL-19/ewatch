# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-08 12:24
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('fa', 'Farsi'), ('en', 'English'), ('ar', 'Arabic')], max_length=2, verbose_name='Language')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified Time')),
                ('about', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='About Election Watch')),
                ('contact_email', models.CharField(blank=True, max_length=64, null=True, verbose_name='Contact Email')),
                ('privacy_policy', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Privacy Policy')),
                ('terms_of_service', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Terms of Service')),
            ],
            options={
                'verbose_name_plural': 'Web Texts',
            },
        ),
    ]
