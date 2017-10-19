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


from ewatch.generics import ReadOnlyViewSet
from serializers import (
    PartySerializer,
    CandidateSerializer,
    IssueSerializer,
    FigureSerializer,
    IssueCategorySerializer,
    IssueStanceChoiceSerializer,
)
from models import (
    Party,
    Candidate,
    Issue,
    IssueCategory,
    IssueStanceChoice,
    Figure,
)


class FigureViewSet(ReadOnlyViewSet):
    """
        View Political Figures
    """

    queryset = Figure.objects.all()
    serializer_class = FigureSerializer
    filter_func = 'text_search'


class PartyViewSet(ReadOnlyViewSet):
    """
        View Political Party
    """

    queryset = Party.objects.all()
    serializer_class = PartySerializer
    filter_func = 'text_search'


class IssueStanceChoiceViewSet(ReadOnlyViewSet):
    """
        Issue Stance Choice
    """

    queryset = IssueStanceChoice.objects.all()
    serializer_class = IssueStanceChoiceSerializer


class IssueCategoryViewSet(ReadOnlyViewSet):
    """
        Issue Category
    """

    queryset = IssueCategory.objects.all()
    serializer_class = IssueCategorySerializer


class IssueViewSet(ReadOnlyViewSet):
    """
        View Issues
    """

    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    filter_func = 'text_search'


class CandidateViewSet(ReadOnlyViewSet):
    """
        View Candidate
    """

    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    filter_func = 'text_search'
