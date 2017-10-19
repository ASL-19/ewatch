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


from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.db import models
from ewatch.generics import (
    SearchableModel,
    OrderedMixin,
)
from ckeditor.fields import RichTextField
import candidate_settings


class Party(SearchableModel, OrderedMixin):
    """
        Model to represent Political parties

        This model is a based on SearchableModel in order to
        facilitate the trigram search.
    """

    logo = models.ImageField(
        upload_to=candidate_settings.LOGO_PATH,
        null=True,
        blank=True,
        verbose_name=_('Logo'))
    link = models.URLField(
        verbose_name=_('Link URL'),
        null=True,
        blank=True)

    def __unicode__(self):

        return self.title

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

        verbose_name_plural = _('Political Parties')


class Figure(SearchableModel, OrderedMixin):
    """
        Model to represent Political figures

        This model is a based on SearchableModel in order to
        facilitate the trigram search.
    """

    photo = models.ImageField(
        upload_to=candidate_settings.LOGO_PATH,
        null=True,
        blank=True,
        verbose_name=_('Photo'))
    link = models.URLField(
        verbose_name=_('Link URL'),
        null=True,
        blank=True)

    def __unicode__(self):

        return self.title

    @property
    def admin_thumbnail(self):
        """
            Return an image to be displayed in admin panel

            Returns:
            An html to image logo if exists or a text of no image otherwise.
        """

        if self.photo:
            return mark_safe("<img src='{}' height='100' />".format(self.photo.url))
        else:
            return "( No Image )"

    class Meta:

        verbose_name_plural = _('Political Figures')


class IssueCategory(models.Model):
    """
        Categories for different issues
    """

    last_modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Modified Time'))
    name = models.CharField(
        max_length=256,
        verbose_name=_('Name'))
    order = models.PositiveIntegerField(
        blank=True,
        null=True,
        unique=True)

    def __unicode__(self):

        return self.name

    class Meta:

        verbose_name_plural = _('Issue Categories')
        ordering = ('order',)


class IssueStanceChoice(models.Model):
    """
        Different Stace a candidate can take on an issue
    """

    last_modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Modified Time'))
    name = models.CharField(
        max_length=1024,
        verbose_name=_('Choice Name'))

    def __unicode__(self):

        return self.name


class Issue(SearchableModel, OrderedMixin):
    """
        Model to represent the issues of concern during election
    """

    category = models.ForeignKey(
        IssueCategory,
        verbose_name=_('Category'),
        related_name='issues')
    order = models.PositiveIntegerField(
        blank=True,
        null=True,
        unique=True)

    def __unicode__(self):

        return self.title

    class Meta:

        ordering = ('order',)


class Candidate(SearchableModel):
    """
        Model to represent Candidates

        This model is a based on SearchableModel in order to
        facilitate the trigram search.
    """

    last_name = models.CharField(
        max_length=512,
        verbose_name=_('Last Name'))
    photo = models.ImageField(
        upload_to=candidate_settings.PHOTO_PATH,
        null=True,
        blank=True,
        verbose_name=_('Picture'))
    bio = RichTextField(
        null=True,
        blank=True,
        verbose_name=_('Biography Summary'))
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Age'))
    birth_place = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        verbose_name=_('Place of Birth'))
    education = RichTextField(
        null=True,
        blank=True,
        verbose_name=_('Education'))
    political_orientation = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Political Orientation'))
    party = models.ManyToManyField(
        'Party',
        related_name='candidate',
        verbose_name=_('Supporting Parties'),
        blank=True)
    figure = models.ManyToManyField(
        'Figure',
        related_name='candidate',
        verbose_name=_('Supporting Figures'),
        blank=True)
    political_background = RichTextField(
        null=True,
        blank=True,
        verbose_name=_('Political Background'))
    military_background = RichTextField(
        null=True,
        blank=True,
        verbose_name=_('Military Background'))
    platform = RichTextField(
        null=True,
        blank=True,
        verbose_name=_('Platform'))
    website = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        verbose_name=_('Website'))
    email = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name=_('Email'))
    telephone = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        verbose_name=_('Telephone'))
    fax = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        verbose_name=_('Fax'))
    facebook = models.URLField(
        verbose_name=_('Facebook URL'),
        null=True,
        blank=True)
    twitter = models.CharField(
        max_length=128,
        verbose_name=_('Twitter Handle'),
        null=True,
        blank=True)
    instagram = models.CharField(
        max_length=128,
        verbose_name=_('Instagram Handle'),
        null=True,
        blank=True)
    telegram = models.CharField(
        max_length=128,
        verbose_name=_('Telegram Handle'),
        null=True,
        blank=True)
    status = models.BooleanField(
        default=True,
        verbose_name=_('Active'))
    status_text = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        verbose_name=_('Status Text'))
    issue = models.ManyToManyField(
        Issue,
        through='IssuesStance')
    publish = models.BooleanField(
        default=True,
        verbose_name=_('Publish'))

    def __unicode__(self):

        return self.title

    @property
    def admin_thumbnail(self):
        """
            Return an image to be displayed in admin panel

            Returns:
            An html to image logo if exists or a text of no image otherwise.
        """

        if self.photo:
            return mark_safe("<img src='{}' height='100' />".format(self.photo.url))
        else:
            return "( No Image )"

    class Meta:

        ordering = ('-status', 'last_name')


class IssuesStance(models.Model):
    """
        Relationship between Issues and Candidate
    """

    last_modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Modified Date'))
    candidate = models.ForeignKey(
        Candidate,
        verbose_name=_('Candidate'))
    issue = models.ForeignKey(
        Issue,
        verbose_name=_('Issue'))
    stance = models.ForeignKey(
        IssueStanceChoice,
        verbose_name=_('Issue Stance'))
    stance_text = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Stance on Issue'))

    class Meta:

        ordering = ('issue__order',)
