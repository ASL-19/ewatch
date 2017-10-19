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


from django.db import models
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework import viewsets
from rest_framework.response import Response
from ewatch.generics import SecureJSONRenderer
from models import WordCloudWord


class WordCloudViewSet(viewsets.ViewSet):
    """
        View Word Cloud words
    """

    renderer_classes = (BrowsableAPIRenderer, SecureJSONRenderer)

    def list(self, request, version, candid):

        if candid is None:
            Response(None)

        queryset = WordCloudWord.objects.filter(entity=candid)

        total = queryset.count()
        if total == 0:
            return Response(None)

        queryset = queryset.values('word') \
            .annotate(
                frequency=models.ExpressionWrapper(
                    models.Count('word') / models.Value(total, output_field=models.FloatField()),
                    output_field=models.FloatField())) \
            .order_by('-frequency')

        return Response(queryset)
