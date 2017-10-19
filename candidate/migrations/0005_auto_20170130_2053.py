# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-30 20:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0004_auto_20170103_2243'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(auto_now=True, verbose_name='Last Modified Time')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='IssueStanceChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(auto_now=True, verbose_name='Last Modified Time')),
                ('name', models.CharField(max_length=1024, verbose_name='Choice Name')),
            ],
        ),
        migrations.AddField(
            model_name='issuesstance',
            name='stance_text',
            field=models.TextField(blank=True, null=True, verbose_name='Stance on Issue'),
        ),
        migrations.AlterField(
            model_name='issuesstance',
            name='stance',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='candidate.IssueStanceChoice', verbose_name='Issue Stance'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='issue',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='candidate.IssueCategory', verbose_name='Category'),
            preserve_default=False,
        ),
    ]