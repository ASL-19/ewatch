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
    Party,
    Candidate,
    IssuesStance,
    Issue,
    Figure,
    IssueStanceChoice,
    IssueCategory
)


class FigureSerializer(serializers.HyperlinkedModelSerializer):
    """
        Political Figure deserializer
    """

    class Meta:

        model = Figure
        depth = 1
        fields = (
            'id',
            'url',
            'last_modified_date',
            'title',
            'content',
            'tag',
            'photo',
            'link')


class FigureSearchSerializer(serializers.HyperlinkedModelSerializer):
    """
        Political Figure Search deserializer
    """

    similarity = serializers.DecimalField(max_digits=6, decimal_places=3)

    class Meta:

        model = Figure
        depth = 1
        fields = (
            'id',
            'url',
            'last_modified_date',
            'similarity',
            'title',
            'content',
            'tag',
            'photo',
            'link')


class PartySerializer(serializers.HyperlinkedModelSerializer):
    """
        Political Party deserializer
    """

    class Meta:

        model = Party
        depth = 1
        fields = (
            'id',
            'url',
            'last_modified_date',
            'title',
            'content',
            'tag',
            'logo',
            'link')


class PartySearchSerializer(serializers.HyperlinkedModelSerializer):
    """
        Political Party Search results deserializer
    """

    similarity = serializers.DecimalField(max_digits=6, decimal_places=3)

    class Meta:

        model = Party
        depth = 1
        fields = (
            'id',
            'url',
            'last_modified_date',
            'similarity',
            'title',
            'content',
            'tag',
            'logo',
            'link')


class IssueStanceSerializer(serializers.ModelSerializer):
    """
        Issue Stance Serialzier
    """

    class Meta:

        model = IssuesStance
        depth = 1
        fields = (
            'id',
            'last_modified_date',
            'issue',
            'stance',
            'stance_text')


class IssueSearchSerializer(serializers.HyperlinkedModelSerializer):
    """
        Issue deserializer
    """

    class Meta:

        model = Issue
        depth = 1
        fields = (
            'id',
            'url',
            'last_modified_date',
            'similarity',
            'title',
            'content',
            'order',
            'tag')


class IssueCategorySerializer(serializers.HyperlinkedModelSerializer):
    """
        Issue Category Serializer
    """

    class Meta:

        model = IssueCategory
        depth = 1
        fields = (
            'id',
            'url',
            'last_modified_date',
            'order',
            'name')


class IssueStanceChoiceSerializer(serializers.HyperlinkedModelSerializer):
    """
        Issue Stance Choices serializer
    """

    class Meta:

        model = IssueStanceChoice
        depth = 1
        fields = (
            'id',
            'url',
            'last_modified_date',
            'name')


class IssueSerializer(serializers.ModelSerializer):
    """
        Issue deserializer
    """

    class Meta:

        model = Issue
        read_only = True
        fields = (
            'id',
            'last_modified_date',
            'title',
            'content',
            'order',
            'tag')


class CandidateListSerializer(serializers.HyperlinkedModelSerializer):
    """
        Candidate List deserializer
    """

    class Meta:

        model = Candidate
        depth = 1
        fields = (
            'id',
            'url',
            'last_modified_date',
            'title',
            'content',
            'last_name',
            'tag',
            'photo',
            'status',
            'status_text')


class CandidateSerializer(serializers.HyperlinkedModelSerializer):
    """
        Candidate deserializer
    """

    party = PartySerializer(many=True, read_only=True)
    issue_stance = IssueStanceSerializer(source='issuesstance_set', many=True)

    class Meta:

        model = Candidate
        depth = 1
        fields = (
            'id',
            'url',
            'last_modified_date',
            'title',
            'content',
            'last_name',
            'tag',
            'photo',
            'bio',
            'age',
            'birth_place',
            'education',
            'political_orientation',
            'party',
            'figure',
            'political_background',
            'military_background',
            'platform',
            'website',
            'email',
            'telephone',
            'fax',
            'facebook',
            'twitter',
            'instagram',
            'telegram',
            'status',
            'status_text',
            'issue_stance')


class CandidateSearchSerializer(serializers.HyperlinkedModelSerializer):
    """
        Candidate Search results deserializer
    """

    similarity = serializers.DecimalField(max_digits=6, decimal_places=3)
    issue_stance = IssueStanceSerializer(many=True, read_only=True)

    class Meta:

        model = Candidate
        depth = 1
        fields = (
            'id',
            'url',
            'last_modified_date',
            'similarity',
            'title',
            'content',
            'tag',
            'photo',
            'bio',
            'age',
            'birth_place',
            'education',
            'political_orientation',
            'party',
            'figure',
            'political_background',
            'military_background',
            'platform',
            'website',
            'email',
            'telephone',
            'fax',
            'facebook',
            'twitter',
            'instagram',
            'telegram',
            'status',
            'status_text',
            'issue_stance')
