# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-20 16:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('candidate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NamedEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(auto_now=True, verbose_name='Last Modified Date')),
                ('name', models.CharField(max_length=1024, verbose_name='Named Entity')),
            ],
            options={
                'verbose_name_plural': 'Named Entities',
            },
        ),
        migrations.CreateModel(
            name='StopWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(auto_now=True, verbose_name='Last Modified Date')),
                ('word', models.CharField(max_length=256, verbose_name='Stop Word')),
            ],
            options={
                'verbose_name_plural': 'Stop Words',
            },
        ),
        migrations.CreateModel(
            name='WordCloudText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(auto_now=True, verbose_name='Last Modified Date')),
                ('name', models.CharField(max_length=1024, verbose_name='Name')),
                ('text', models.TextField(verbose_name='Text')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wordcloud_text', to='candidate.Candidate', verbose_name='Candidate')),
            ],
            options={
                'verbose_name_plural': 'Word Cloud Texts',
            },
        ),
        migrations.CreateModel(
            name='WordCloudWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(auto_now=True, verbose_name='Last Modified Date')),
                ('word', models.CharField(max_length=256, verbose_name='Word')),
                ('org_word', models.CharField(max_length=256, verbose_name='Original Word')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wordcloud_word', to='candidate.Candidate', verbose_name='Candidate')),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='word', to='wordcloud.WordCloudText')),
            ],
            options={
                'verbose_name_plural': 'Word Cloud Words',
            },
        ),
    ]
