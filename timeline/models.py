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
from django_jalali.db import models as jmodels
from ewatch.generics import SearchableModel
from blog.models import Category
from candidate.models import Candidate
import timeline_settings


class Timeline(SearchableModel):
    """
        Model to represent Timeline
    """

    timestamp = jmodels.jDateTimeField(
        verbose_name=_('Time'))
    category = models.ForeignKey(
        Category,
        related_name='timeline',
        null=True,
        blank=True)
    photo = models.ImageField(
        upload_to=timeline_settings.LOGO_PATH,
        null=True,
        blank=True,
        verbose_name=_('Image'))
    photo_caption = models.CharField(
        max_length=2048,
        null=True,
        blank=True,
        verbose_name=_('Image Caption'))
    candidate_tag = models.ManyToManyField(
        Candidate,
        related_name='timeline_news',
        verbose_name='Candidates\' tag',
        blank=True)
    breaking = models.BooleanField(
        default=False)
