# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-08 12:24
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('candidate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(auto_now=True, verbose_name='Last Modified Time')),
                ('name', models.CharField(max_length=32, verbose_name='Category Name')),
                ('logo', models.ImageField(blank=True, null=True, upload_to=b'blog/logos', verbose_name='Photo')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_date', models.DateTimeField(auto_now=True, verbose_name='Comment Date')),
                ('email', models.CharField(max_length=256, verbose_name='Email')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('title', models.CharField(max_length=512, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('approved', models.BooleanField(default=False, verbose_name='Approved')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(auto_now=True, verbose_name='Last Modified Time')),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Content')),
                ('tag', models.TextField(blank=True, max_length=8192, null=True, verbose_name='Tags')),
                ('published_date', models.DateTimeField(verbose_name='Published Time')),
                ('summary', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Summary')),
                ('slug', models.SlugField(max_length=128)),
                ('status', models.CharField(choices=[('p', 'published'), ('d', 'draft')], default='p', max_length=1)),
                ('comment_allowed', models.BooleanField(default=False, verbose_name='Comments Allowed')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('candidate_tag', models.ManyToManyField(related_name='blog_posts', to='candidate.Candidate', verbose_name="Candidates' tag")),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post', to='blog.Category', verbose_name='Category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='blog.Post', verbose_name='Post'),
        ),
    ]
