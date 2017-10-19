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


from django.contrib import admin
from models import (
    Questionnaire,
    Choice,
    ChoiceSet,
    QuestionSet,
    QuestionCategory,
    Question,
    Participant,
    Response,
)


class ResponseAdmin(admin.ModelAdmin):
    """
        Response change panel

        This class only let user moderate reviews
    """

    def has_add_permission(self, request):
        return False


class ParticipantAdmin(admin.ModelAdmin):
    """
        Participant change panel

        This class only let user moderate reviews
    """

    def has_add_permission(self, request):
        return False


class QuestionInline(admin.StackedInline):
    """
        Question add/change panel to be inserted inline
    """

    model = Question
    extra = 1


class QuestionSetInline(admin.StackedInline):
    """
        Question Set add/change panel to be inserted inline
    """

    model = QuestionSet
    extra = 1


class QuestionSetAdmin(admin.ModelAdmin):
    """
        Question Set add/change panel
    """

    list_display = [
        'order',
        'name',
    ]

    inlines = [
        QuestionInline,
    ]

    ordering = ['order']


class QuestionnaireAdmin(admin.ModelAdmin):
    """
        Questionnaire add/change panel
    """

    inlines = [
        QuestionSetInline,
    ]


class QuestionAdmin(admin.ModelAdmin):
    """
        Question add/change panel
    """

    list_display = [
        'questionnaire',
        'order',
        'question_set',
        'text',
    ]

    ordering = ['order']


class ChoiceSetAdmin(admin.ModelAdmin):
    """
        Multiple Choice questions' choice sets add/change panel
    """

    list_display = [
        'name',
    ]


class ChoiceAdmin(admin.ModelAdmin):
    """
        Multiple Choice questions' choice add/change panel
    """

    list_display = [
        'choice_set',
        'order',
        'value',
        'text',
    ]

    ordering = ['choice_set', 'order']


class QuestionCategoryAdmin(admin.ModelAdmin):
    """
        Questions' category add/change panel
    """

    list_display = [
        'name',
    ]


admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(ChoiceSet, ChoiceSetAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin)
admin.site.register(QuestionCategory, QuestionCategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Response, ResponseAdmin)
