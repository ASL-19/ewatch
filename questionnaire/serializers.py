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


from rest_framework import serializers
from models import (
    Choice,
    ChoiceSet,
    Question,
    QuestionCategory,
    QuestionSet,
    Questionnaire,
    Response,
    Participant,
)


class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    """
        Choice deserializer
    """

    class Meta:

        model = Choice
        depth = 1
        fields = (
            'id',
            'url',
            'last_modified_date',
            'text',
            'order',
            'value')


class ChoiceSetSerializer(serializers.HyperlinkedModelSerializer):
    """
        Choice Set deserializer
    """

    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:

        model = ChoiceSet
        depth = 1
        fields = (
            'id',
            'name',
            'choices',
        )


class QuestionCategorySerializer(serializers.HyperlinkedModelSerializer):
    """
        Question category deserializer
    """

    class Meta:
        model = QuestionCategory
        fields = (
            'id',
            'last_modified_date',
            'name')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    """
        Question deserializer
    """

    class Meta:

        model = Question
        depth = 1
        fields = (
            'id',
            'url',
            'last_modified_date',
            'question_set',
            'choice_set',
            'category',
            'text',
            'extra',
            'qtype',
            'order',
            'required',
            'enabled')


class QuestionSetSerializer(serializers.HyperlinkedModelSerializer):
    """
        Question Set deserializer
    """

    question = QuestionSerializer(many=True, read_only=True)

    class Meta:

        model = QuestionSet
        depth = 1
        fields = (
            'id',
            'url',
            'last_modified_date',
            'questionnaire',
            'order',
            'name',
            'description',
            'question')


class QuestionnaireSerializer(serializers.HyperlinkedModelSerializer):
    """
        Questionnaire deserializer
    """

    class Meta:

        model = Questionnaire
        depth = 1
        fields = (
            'id',
            'url',
            'last_modified_date',
            'name',
            'description',
            'question_set')


class ResponseSerializer(serializers.ModelSerializer):
    """
        Questionnaire response deserializer
    """

    question = serializers.HyperlinkedRelatedField(queryset=Question.objects.all(), view_name='question-detail')
    participant = serializers.HyperlinkedRelatedField(queryset=Participant.objects.all(), view_name='participantdetail-detail')

    class Meta:

        model = Response
        depth = 1
        fields = (
            'last_modified_date',
            'creation_date',
            'question',
            'participant',
            'answer')


class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
    """
        Participant deserializer
    """

    class Meta:

        model = Participant
        depth = 1
        fields = (
            'last_modified_date',
            'id',
            'first_name',
            'last_name',
            'email',
            'gender',
            'address',
            'age',
            'married',
            'education',
            'income',
            'income_currency',
            'ethnicity',
            'religion')
