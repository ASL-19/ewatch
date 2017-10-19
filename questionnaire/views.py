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


from django.db.models import Sum, Count
from rest_framework.response import Response as DRFResponse
from rest_framework.renderers import BrowsableAPIRenderer
from ewatch.generics import (
    ReadOnlyViewSet,
    SecureJSONRenderer
)
from rest_framework import (
    viewsets,
    mixins,
    permissions,
)
from serializers import (
    ChoiceSerializer,
    ChoiceSetSerializer,
    QuestionnaireSerializer,
    QuestionSetSerializer,
    QuestionSerializer,
    ResponseSerializer,
    ParticipantSerializer,
    QuestionCategorySerializer,
)
from models import (
    Choice,
    ChoiceSet,
    Questionnaire,
    QuestionSet,
    Question,
    QuestionCategory,
    Response,
    Participant,
)


class ChoiceSetViewSet(ReadOnlyViewSet):
    """
        View Choices
    """

    queryset = ChoiceSet.objects.all()
    serializer_class = ChoiceSetSerializer


class ChoiceViewSet(ReadOnlyViewSet):
    """
        View Choices
    """

    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class QuestionnaireViewSet(ReadOnlyViewSet):
    """
        View Questionnaire
    """

    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer


class QuestionSetViewSet(ReadOnlyViewSet):
    """
        View Question Sets
    """

    queryset = QuestionSet.objects.all()
    serializer_class = QuestionSetSerializer


class QuestionCategoryViewSet(ReadOnlyViewSet):
    """
        View Question Categories
    """

    queryset = QuestionCategory.objects.all()
    serializer_class = QuestionCategorySerializer


class QuestionViewSet(ReadOnlyViewSet):
    """
        View Questions
    """

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ResponseViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
        Create Responses
    """

    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    renderer_classes = (BrowsableAPIRenderer, SecureJSONRenderer)


class ParticipantViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
        Create Participants
    """

    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    renderer_classes = (BrowsableAPIRenderer, SecureJSONRenderer)


class AllowNone(permissions.BasePermission):
    """
        Allow access to none
    """

    def has_permission(self, request, view):
        return False


class ParticipantDetailViewSet(ReadOnlyViewSet):
    """
        Create Participants
    """

    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [AllowNone]


class ResultViewSet(viewsets.ViewSet):
    """
        Questionnaire results by participant
    """

    renderer_classes = (BrowsableAPIRenderer, SecureJSONRenderer)
    MAXVALUE = 5.0
    MINVALUE = 1.0

    def list(self, request, version, pid):

        def calc_all():

            queryset = Response.objects \
                       .prefetch_related('question', 'question__category', 'question__question_set') \
                       .values('question') \
                       .annotate(sum_answer=Sum('answer'), count_answer=Count('answer'))
            questions = Question.objects.all()

            result = {}

            for q in queryset:
                question = questions.get(id=q['question'])
                setname = question.question_set.name
                catname = question.category.name
                if setname not in result:
                    result[setname] = {}
                if catname not in result[setname]:
                    result[setname][catname] = {}
                    result[setname][catname]['sum'] = q['sum_answer']
                    result[setname][catname]['count'] = q['count_answer']
                    cnt = float(result[setname][catname]['count'])
                    if question.qtype == 'MCH':
                        result[setname][catname]['normal'] = (float(result[setname][catname]['sum']) - self.MINVALUE * cnt) / ((self.MAXVALUE - self.MINVALUE) * cnt)
                    elif question.qtype == 'PER':
                        result[setname][catname]['normal'] = float(q['sum_answer'])/(float(result[setname][catname]['count']) * 100.0)
                else:
                    result[setname][catname]['sum'] += q['sum_answer']
                    result[setname][catname]['count'] += q['count_answer']
                    cnt = float(result[setname][catname]['count'])
                    if question.qtype == 'MCH':
                        result[setname][catname]['normal'] = (float(result[setname][catname]['sum']) - self.MINVALUE * cnt) / ((self.MAXVALUE - self.MINVALUE) * cnt)
                    elif question.qtype == 'PER':
                        result[setname][catname]['normal'] = float(result[setname][catname]['sum'])/(float(result[setname][catname]['count']) * 100.0)
    
            return result

        queryset = None
        if pid is None:
            return DRFResponse({})

        queryset = Response.objects \
            .filter(participant=pid) \
            .prefetch_related('question', 'question__category', 'question__question_set')

        # totals = Question.objects.all() \
        #     .values('question_set','category') \
        #     .annotate(total=Count('id'))

        result = {}
        for q in queryset:
            setname = q.question.question_set.name
            catname = q.question.category.name
            if setname not in result:
                result[setname] = {}
            if catname not in result[setname]:
                result[setname][catname] = {}
                result[setname][catname]['sum'] = q.answer
                result[setname][catname]['count'] = 1
                if q.question.qtype == 'MCH':
                    result[setname][catname]['normal'] = (float(q.answer) - self.MINVALUE) / self.MAXVALUE
                elif q.question.qtype == 'PER':
                    result[setname][catname]['normal'] = float(q.answer) / 100.0
            else:
                result[setname][catname]['sum'] += q.answer
                result[setname][catname]['count'] += 1
                cnt = float(result[setname][catname]['count'])
                result[setname][catname]['normal'] = (float(result[setname][catname]['sum']) - self.MINVALUE * cnt) / ((self.MAXVALUE - self.MINVALUE) * cnt)

        allresults = calc_all()

        results = {
            'all': allresults,
            'participant': result,
        }

        return DRFResponse(results)
