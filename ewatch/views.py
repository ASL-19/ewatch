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


from operator import methodcaller
from rest_framework import viewsets
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.response import Response
from blog.views import PostViewSet
from blog.serializers import PostSearchSerializer
from candidate.views import (
    CandidateViewSet,
    FigureViewSet,
    PartyViewSet,
    IssueViewSet,
)
from candidate.serializers import (
    CandidateSearchSerializer,
    FigureSearchSerializer,
    PartySearchSerializer,
    IssueSearchSerializer,
)
from timeline.views import TimelineViewSet
from timeline.serializers import TimelineSearchSerializer
from timeline.models import Timeline
from blog.models import Post
from candidate.models import (
    Candidate,
    Issue,
    Party,
    Figure
)
from ewatch.generics import SecureJSONRenderer


class DetailSearchViewSet(viewsets.ViewSet):
    """
        View Search for detailed results of trigram search
    """

    renderer_classes = (BrowsableAPIRenderer, SecureJSONRenderer)

    def list(self, request, *args, **kwargs):
        """
            List method to return response to GET requests for search

            It checks for 'q' parameters in query params for trigram search
            and searches different models (defined as searchable) for the 'q'
            keyword

            Args:
            request: The request object from client
            *args, **kwargs: Extra arguments passed into the function

            Returns:
            Response object containing the result of the request.
        """

        keyword = self.request.query_params.get('q', None)
        if keyword is None:
            Response(None)

        resp_data = {}

        results = PostViewSet.queryset.text_search(
            keyword=keyword,
            fields_list=['summary'])
        resp_data['posts'] = PostSearchSerializer(
            results,
            many=True,
            context={'request': request}).data

        results = CandidateViewSet.queryset.text_search(
            keyword=keyword,
            fields_list=[
                'bio',
                'political_orientation',
                'political_background',
                'military_background',
                'platform',
                'status_text'])
        resp_data['candidates'] = CandidateSearchSerializer(
            results,
            many=True,
            context={'request': request}).data

        results = FigureViewSet.queryset.text_search(
            keyword=keyword)
        resp_data['figures'] = FigureSearchSerializer(
            results,
            many=True,
            context={'request': request}).data

        results = PartyViewSet.queryset.text_search(
            keyword=keyword)
        resp_data['parties'] = PartySearchSerializer(
            results,
            many=True,
            context={'request': request}).data

        results = TimelineViewSet.queryset.text_search(
            keyword=keyword)
        resp_data['timelines'] = TimelineSearchSerializer(
            results,
            many=True,
            context={'request': request}).data

        results = IssueViewSet.queryset.text_search(
            keyword=keyword)
        resp_data['issues'] = IssueSearchSerializer(
            results,
            many=True,
            context={'request': request}).data

        return Response(resp_data)


class CandidateSearchViewSet(viewsets.ViewSet):
    """
        View search in candidate tags
    """

    renderer_classes = (BrowsableAPIRenderer, SecureJSONRenderer)

    def list(self, request, *args, **kwargs):
        """
            List method to return response to GET requests for search

            It checks for 'q' parameters in query params for trigram search
            and searches different models

            Args:
            request: The request object from client
            *args, **kwargs: Extra arguments passed into the function

            Returns:
            Response object containing the result of the request.
        """

        keyword = self.request.query_params.get('q', None)

        resp_data = {}

        results = PostViewSet.queryset.tag_search(
            keyword=keyword,
            tag_fields=['candidate_tag__title'])
        resp_data['posts'] = PostSearchSerializer(
            results,
            many=True,
            context={'request': request}).data

        results = TimelineViewSet.queryset.tag_search(
            keyword=keyword,
            tag_fields=['candidate_tag__title'])
        resp_data['timelines'] = TimelineSearchSerializer(
            results,
            many=True,
            context={'request': request}).data

        return Response(resp_data)


class TagViewSet(viewsets.ViewSet):
    """
        View tags for offices
    """

    renderer_classes = (BrowsableAPIRenderer, SecureJSONRenderer)

    def list(self, request, version):

        queryset = None
        obj = request.query_params.get('obj', None)
        if obj is not None:
            if obj.lower() == 'post':
                queryset = Post.objects.values_list('tag', flat=True)
            elif obj.lower() == 'timeline':
                queryset = Timeline.objects.values_list('tag', flat=True)
            elif obj.lower() == 'party':
                queryset = Party.objects.values_list('tag', flat=True)
            elif obj.lower() == 'figure':
                queryset = Figure.objects.values_list('tag', flat=True)
            elif obj.lower() == 'issue':
                queryset = Issue.objects.values_list('tag', flat=True)
            elif obj.lower() == 'candidate':
                queryset = Candidate.objects.values_list('tag', flat=True)

        if queryset is None:
            return Response(None)
        else:
            tag_list = map(methodcaller('split', ','), [x for x in list(queryset) if x is not None])
            tags = set([y.strip() for x in tag_list for y in x if len(y) > 0])
            return Response({'tags': tags})
