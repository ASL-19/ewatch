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
from ckeditor_uploader.fields import RichTextUploadingField


class Questionnaire(models.Model):
    """
        Model to represent a Questionnaire
    """

    last_modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Modified Date'))
    name = models.CharField(
        max_length=512,
        verbose_name=_('Name'))
    description = RichTextUploadingField(
        verbose_name=_('Description'))

    @property
    def question_set(self):
        """
            Question Sets in the Questionnaire
        """

        return QuestionSet.objects.filter(questionnaire=self.id)

    def __unicode__(self):

        return self.name


class ChoiceSet(models.Model):
    """
        Model to represent a choise set for multiple choise
        questions.
    """

    last_modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Modified Date'))
    name = models.CharField(
        max_length=128,
        verbose_name=_('Name'))

    def __unicode__(self):

        return self.name


class Choice(models.Model):
    """
        Model to represent choices for multiple choice questions
    """

    last_modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Modified Date'))
    text = models.CharField(
        max_length=128,
        verbose_name=_('Text'))
    order = models.PositiveIntegerField(
        verbose_name=_('Order'))
    value = models.IntegerField(
        verbose_name=_('Value'))
    choice_set = models.ForeignKey(
        ChoiceSet,
        verbose_name=_('Choice Set'),
        related_name='choices')

    def __unicode__(self):

        return self.text

    class Meta:

        unique_together = [
            'order',
            'choice_set'
        ]


class QuestionSet(models.Model):
    """
        Model to represent Question sets
    """

    last_modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Modified Date'))
    questionnaire = models.ForeignKey(
        Questionnaire,
        verbose_name=_('Questionnaire'),
        related_name='question_set',
        db_index=True)
    order = models.PositiveIntegerField(
        verbose_name=_('Order'),
        unique=True)
    name = models.CharField(
        max_length=512,
        verbose_name=_('Name'))
    description = RichTextUploadingField(
        verbose_name=_('Description'))

    @property
    def question(self):
        """
            Questions in this question set
        """

        return Question.objects.filter(question_set=self.id)

    def __unicode__(self):

        return self.name


class QuestionCategory(models.Model):
    """
        Model to represent question categories
    """

    last_modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Modified Date'))
    name = models.CharField(
        max_length=256,
        verbose_name=_('Category Name'))

    def __unicode__(self):

        return self.name

    class Meta:

        verbose_name_plural = 'Question Categories'


class Question(models.Model):
    """
        Models to represent Questions
    """

    QUESTION_CHOICES = (
        ('MCH', 'Multiple Choice'),
        ('PER', 'Percentage'),
        ('TXT', 'Text'),
    )

    last_modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Modified Date'))
    question_set = models.ForeignKey(
        QuestionSet,
        verbose_name=_('Question Set'),
        related_name='question',
        db_index=True)
    choice_set = models.ForeignKey(
        ChoiceSet,
        verbose_name=_('Choice Set'),
        related_name='question')
    category = models.ForeignKey(
        QuestionCategory,
        related_name='question',
        verbose_name=_('Category'))
    text = RichTextUploadingField(
        verbose_name=_('Question Text'))
    extra = RichTextUploadingField(
        verbose_name=_('Extra Information'),
        null=True,
        blank=True)
    qtype = models.CharField(
        max_length=3,
        choices=QUESTION_CHOICES,
        verbose_name=_('Question Type'))
    order = models.PositiveIntegerField(
        verbose_name=_('Order'))
    required = models.BooleanField(
        default=True)
    enabled = models.BooleanField(
        default=True)

    def questionnaire(self):
        """
            A helper method to return Questionnaire for Question Sets

            Returns:
            questionnaire associated with this Question set
        """

        return self.question_set.questionnaire

    class Meta:

        unique_together = [
            'order',
            'question_set',
        ]


class Participant(models.Model):
    """
        Model to represent Participants of questionnaire
    """

    GENDER_CHOICES = (
        ('unset', _('Unset')),
        ('male', _('male')),
        ('female', _('female'))
    )
    MARRITAL_STATUS_CHOICES = (
        ('married', _('Married')),
        ('single', _('Single (Never Married)')),
        ('divorced', _('Divorced')),
        ('widowed', _('Widowed'))
    )
    EDUCATION_LEVEL_CHOICES = (
        ('nodiploma', _('No Diploma')),
        ('highschool', _('High School Graduate')),
        ('bachelor', _('Bachelor Degree')),
        ('masters', _('Master Degree')),
        ('phd', _('PhD')),
        ('hozeh', _('Hozeh Graduated')),
        ('other', _('Other'))
    )
    INCOME_CURRENCY_CHOICES = (
        ('toman', _('Toman')),
        ('dollar', _('Dollar')),
        ('euro', _('Euro')),
        ('other', _('Other'))
    )
    ETHNICAL_GROUP_CHOICES = (
        ('persian', _('Persian')),
        ('azerbaijani', _('Azerbaijani - Turk')),
        ('kurd', _('Kurd')),
        ('lur', _('Lur')),
        ('arab', _('Arab')),
        ('baloch', _('Baloch')),
        ('turkmen', _('Turkmen')),
        ('other', _('Other')),
        ('noethnicity', _('I don\'t believe in ethnical category'))
    )
    RELIGIOUS_AFFILIATION_CHOICES = (
        ('shia', _('Muslim - Shi\'a')),
        ('sunni', _('Muslim - Sunni')),
        ('christian', _('Christian')),
        ('jew', _('Jew')),
        ('zoroastrian', _('Zoroastrian')),
        ('bahai', _('Baha\'i')),
        ('sabian', _('Sabian')),
        ('ahlehaqq', _('Ahl-e Haqq')),
        ('other', _('Other')),
        ('noreligion', _('I don\'t believe in religion'))
    )

    last_modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Modified Date'))
    first_name = models.CharField(
        max_length=256,
        null=True,
        blank=True)
    last_name = models.CharField(
        max_length=256,
        null=True,
        blank=True)
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_('Email Address'))
    gender = models.CharField(
        max_length=8,
        verbose_name=_('Gender'),
        choices=GENDER_CHOICES)
    address = models.CharField(
        max_length=2048,
        verbose_name=_('Address'))
    age = models.PositiveIntegerField(
        verbose_name=_('Age'))
    married = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        choices=MARRITAL_STATUS_CHOICES,
        verbose_name=_('Married'))
    education = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        choices=EDUCATION_LEVEL_CHOICES,
        verbose_name=_('Education'))
    income = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Income Value'))
    income_currency = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        choices=INCOME_CURRENCY_CHOICES,
        verbose_name=_('Income Currency'))
    ethnicity = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        choices=ETHNICAL_GROUP_CHOICES,
        verbose_name=_('Ethnicity'))
    religion = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        choices=RELIGIOUS_AFFILIATION_CHOICES,
        verbose_name=_('Religious Affiliation'))

    def __unicode__(self):

        return self.gender + " of " + str(self.age) + " at " + self.address


class Response(models.Model):
    """
        Model to represent responses
    """

    last_modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Modified Date'))
    creation_date = models.DateTimeField(
        auto_now_add=True)
    question = models.ForeignKey(
        Question,
        verbose_name=_('Question'),
        related_name='response')
    participant = models.ForeignKey(
        Participant,
        verbose_name=_('Participant'),
        related_name='participant',
        db_index=True)
    answer = models.IntegerField(
        verbose_name=_('Answer'))

    class Meta:

        unique_together = [
            'question',
            'participant'
        ]

    def __unicode__(self):

        return str(self.participant)
