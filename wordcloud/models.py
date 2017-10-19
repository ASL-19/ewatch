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
import re
import string
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models.signals import (
    post_save,
    post_delete,
)
from django.utils.html import strip_tags
from candidate.models import Candidate
from signals import (
    wordcloudtext_saved,
    stopword_added,
    stopword_deleted,
    namedentity_changed,
)


class WordCloudText(models.Model):
    """
        Models to represent Word Cloud Texts
    """

    last_modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Modified Date'))
    name = models.CharField(
        max_length=1024,
        verbose_name=_('Name'))
    text = models.TextField(
        verbose_name=_('Text'))
    entity = models.ForeignKey(
        Candidate,
        verbose_name=_('Candidate'),
        related_name='wordcloud_text')
    link = models.URLField(
        max_length=1024,
        null=True,
        blank=True,
        verbose_name=_('Original URL'))

    def clean(self):
        """
            Remove tags and normalize the text
            This only works for Farsi texts
        """
        super(WordCloudText, self).clean()
        replace_pattern = re.compile(r'[\s' + string.punctuation + ']+')
        self.text = strip_tags(re.sub(replace_pattern, ' ', self.text))
        self.text = re.sub(r'[‌]+', '‌', self.text)

    def __unicode__(self):

        return self.name

    class Meta:

        verbose_name_plural = _('Word Cloud Texts')


post_save.connect(wordcloudtext_saved, sender=WordCloudText)


class StopWord(models.Model):
    """
        Model to represent Stop Words to be removed from Text
    """

    last_modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Modified Date'))
    word = models.CharField(
        max_length=256,
        verbose_name=_('Stop Word'))

    def __unicode__(self):

        return self.word

    class Meta:

        verbose_name_plural = _('Stop Words')


post_save.connect(stopword_added, sender=StopWord)
post_delete.connect(stopword_deleted, sender=StopWord)


class WordCloudWord(models.Model):
    """
        Model to represent all the words from texts

        This acts as an intermdiate table and admins will not
        change this table.
    """

    last_modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Modified Date'))
    word = models.CharField(
        max_length=256,
        verbose_name=_('Word'))
    org_word = models.CharField(
        max_length=256,
        verbose_name=_('Original Word'))
    text = models.ForeignKey(
        WordCloudText,
        related_name='word')
    entity = models.ForeignKey(
        Candidate,
        verbose_name=_('Candidate'),
        related_name='wordcloud_word')

    def __unicode__(self):

        return self.word

    class Meta:

        verbose_name_plural = _('Word Cloud Words')


class NamedEntity(models.Model):
    """
        Model to represent the Named Entities in the texts. This can
        be from any corpus, but by the time of the development of
        this project we could not find any good ones for Farsi.
    """

    last_modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Modified Date'))
    name = models.CharField(
        max_length=1024,
        verbose_name=_('Named Entity'))

    def __unicode__(self):

        return self.name

    def clean(self):
        """
            Remove tags and normalize the text
            This only works for Farsi texts
        """
        super(NamedEntity, self).clean()
        replace_pattern = re.compile(r'[\s' + string.punctuation + ']+')
        self.name = strip_tags(re.sub(replace_pattern, ' ', self.name))
        self.name = re.sub(r'[‌]+', '‌', self.name)

    class Meta:

        verbose_name_plural = _('Named Entities')

post_save.connect(namedentity_changed, sender=NamedEntity)
post_delete.connect(namedentity_changed, sender=NamedEntity)
