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
from django.db import models
from ckeditor.fields import RichTextField


class Text(models.Model):
    """
        This class defines an API model to provide texts such as privacy policy,
        About, Contact information, etc.

        The class has provision for 3 languages for each text.
    """

    LANGUAGE_CHOICES = (
        ('fa', 'Farsi'),
        ('en', 'English'),
        ('ar', 'Arabic'))

    language = models.CharField(
        max_length=2,
        verbose_name=_('Language'),
        choices=LANGUAGE_CHOICES)
    last_modified = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Modified Time'))
    about = RichTextField(
        null=True,
        blank=True,
        verbose_name=_('About Election Watch'))
    contact_email = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name=_('Contact Email'))
    privacy_policy = RichTextField(
        null=True,
        blank=True,
        verbose_name=_('Privacy Policy'))
    terms_of_service = RichTextField(
        null=True,
        blank=True,
        verbose_name=_('Terms of Service'))

    def __unicode__(self):

        return self.language

    class Meta:

        verbose_name_plural = _('Web Texts')
