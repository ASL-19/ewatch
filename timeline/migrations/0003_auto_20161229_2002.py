# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-29 20:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0002_timeline_breaking'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeline',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=b'candidate/logos', verbose_name='Photo'),
        ),
        migrations.AlterField(
            model_name='timeline',
            name='candidate_tag',
            field=models.ManyToManyField(blank=True, related_name='timeline_news', to='candidate.Candidate', verbose_name="Candidates' tag"),
        ),
        migrations.AlterField(
            model_name='timeline',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='timeline', to='blog.Category'),
        ),
    ]
