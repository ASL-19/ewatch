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
from models import Timeline


class TimelineSerializer(serializers.HyperlinkedModelSerializer):
    """
        Timeline deserializer
    """

    candidate_tag = serializers.StringRelatedField(many=True, read_only=True)
    timestamp = serializers.SerializerMethodField()

    def get_timestamp(self, obj):

        return unicode(obj.timestamp)

    class Meta:

        model = Timeline
        depth = 1
        fields = (
            'id',
            'url',
            'last_modified_date',
            'photo',
            'photo_caption',
            'title',
            'content',
            'tag',
            'timestamp',
            'category',
            'candidate_tag')


class TimelineSearchSerializer(serializers.HyperlinkedModelSerializer):
    """
        Timeline deserializer
    """

    similarity = serializers.DecimalField(max_digits=6, decimal_places=3)
    candidate_tag = serializers.StringRelatedField(many=True, read_only=True)
    timestamp = serializers.SerializerMethodField()

    def get_timestamp(self, obj):

        return unicode(obj.timestamp)

    class Meta:

        model = Timeline
        depth = 1
        fields = (
            'id',
            'url',
            'last_modified_date',
            'photo',
            'photo_caption',
            'similarity',
            'title',
            'content',
            'tag',
            'timestamp',
            'category',
            'candidate_tag')
