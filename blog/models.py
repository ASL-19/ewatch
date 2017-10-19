# -*- coding: utf-8 -*-
# Election Watch - To enable responsive governance and informed engagement with presidential elections
#
# Copyright (C) 2016  ASL19
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.core.management import settings
from django.db import models
from django_jalali.db import models as jmodels
from ckeditor_uploader.fields import RichTextUploadingField
from ewatch.generics import SearchableModel
from candidate.models import Candidate
import blog_settings


class Category(models.Model):
    """
        Model to represent Blog posts' categories.
    """

    last_modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Modified Time'))
    name = models.CharField(
        max_length=32,
        verbose_name=_('Category Name'),
        null=False,
        blank=False)
    logo = models.ImageField(
        upload_to=blog_settings.LOGO_PATH,
        null=True,
        blank=True,
        verbose_name=_('Photo'))

    def __unicode__(self):

        return self.name

    @property
    def admin_thumbnail(self):
        """
            Return an image to be displayed in admin panel

            Returns:
            An html to image logo if exists or a text of no image otherwise.
        """

        if self.logo:
            return mark_safe("<img src='{}' height='100' />".format(self.logo.url))
        else:
            return "( No Image )"

    class Meta:

        verbose_name_plural = _('Categories')


class Post(SearchableModel):
    """
        Model to represent the blog posts

        This model is a based on SearchableModel in order to
        facilitate the trigram search.
    """

    POST_STATUS_CHOICES = (
        ('p', 'published'),
        ('d', 'draft'))
    published_date = jmodels.jDateTimeField(
        verbose_name=_('Published Time'))
    category = models.ForeignKey(
        'Category',
        related_name='post',
        verbose_name=_('Category'),
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    summary = RichTextUploadingField(
        null=True,
        blank=True,
        verbose_name=_('Summary'))
    slug = models.SlugField(
        max_length=128,
        unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        related_name='review')
    status = models.CharField(
        max_length=1,
        choices=POST_STATUS_CHOICES,
        default='p')
    comment_allowed = models.BooleanField(
        default=False,
        verbose_name=_('Comments Allowed'))
    candidate_tag = models.ManyToManyField(
        Candidate,
        related_name='blog_posts',
        verbose_name='Candidates\' tag',
        blank=True)
    homepage_feature = models.PositiveIntegerField(
        blank=True,
        null=True,
        unique=True)
    feature_image = models.ImageField(
        upload_to=blog_settings.IMAGE_PATH,
        null=True,
        blank=True,
        verbose_name=_('Feature Image'))
    feature_image_caption = models.CharField(
        max_length=2048,
        null=True,
        blank=True)

    def __unicode__(self):

        return self.title

    def get_post_link(self):
        """
            URL link to posts

            Returns:
            A URL made based on type of the post
        """

        cat = 'analysis'
        if self.category.id == 4 or self.category.id == 6:
            cat = 'educational'
        return '/' + cat + '/' + self.slug


class Comment(models.Model):
    """
        Model to represent the blog comments.
    """

    comment_date = jmodels.jDateTimeField(
        auto_now=True,
        verbose_name=_('Comment Date'))
    email = models.CharField(
        max_length=256,
        verbose_name=_('Email'))
    name = models.CharField(
        max_length=256,
        verbose_name=_('Name'))
    title = models.CharField(
        max_length=512,
        verbose_name=_('Title'))
    content = models.TextField(
        verbose_name=_('Content'))
    approved = models.BooleanField(
        default=False,
        verbose_name=_('Approved'))
    post = models.ForeignKey(
        Post,
        verbose_name=_('Post'),
        related_name='comment')

    def __unicode__(self):

        return self.title
